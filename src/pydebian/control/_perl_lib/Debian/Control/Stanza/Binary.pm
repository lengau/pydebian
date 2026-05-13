package Debian::Control::Stanza::Binary;

use strict;
use warnings;

use base 'Debian::Control::Stanza';

sub fields {
    return qw(
      Package
      Architecture
      Section
      Priority
      Essential
      Depends
      Recommends
      Suggests
      Enhances
      Replaces
      Pre_Depends
      Conflicts
      Breaks
      Provides
      Description
      _short_description
      _long_description
    );
}

sub set {
    my ( $self, $field, $value ) = @_;

    my $result = $self->SUPER::set( $field, $value );
    $field =~ s/-/_/g;

    if ( $field eq 'Description' ) {
        $self->_split_description;
    }
    elsif ( $field eq '_short_description' || $field eq '_long_description' ) {
        $self->_format_description;
    }

    return $result;
}

sub short_description {
    my $self = shift;
    return @_ ? $self->set( '_short_description', shift ) : $self->get('_short_description');
}

sub long_description {
    my $self = shift;
    return @_ ? $self->set( '_long_description', shift ) : $self->get('_long_description');
}

sub _format_description {
    my $self = shift;

    my $short = $self->get('_short_description');
    my $long = $self->get('_long_description');

    if ( defined $long ) {
        $long =~ s/\n\n/\n.\n/sg;
        $long =~ s/^/ /mg;
    }

    $self->{_values}{Description} = join( "\n", grep { defined $_ && $_ ne '' } ( $short, $long ) );
    if ( !grep { $_ eq 'Description' } @{ $self->{_order} } ) {
        push @{ $self->{_order} }, 'Description';
    }

    return;
}

sub _split_description {
    my $self = shift;

    my $description = $self->get('Description');
    return unless defined $description;

    my ( $short, $long ) = split( /\n/, $description, 2 );
    if ( defined $long ) {
        $long =~ s/^ //mg;
        $long =~ s/^\.$//mg;
    }

    $self->{_values}{'-short-description'} = $short;
    $self->{_values}{'-long-description'} = $long;

    if ( !grep { $_ eq '-short-description' } @{ $self->{_order} } ) {
        push @{ $self->{_order} }, '-short-description';
    }
    if ( defined $long && !grep { $_ eq '-long-description' } @{ $self->{_order} } ) {
        push @{ $self->{_order} }, '-long-description';
    }

    return;
}

1;
