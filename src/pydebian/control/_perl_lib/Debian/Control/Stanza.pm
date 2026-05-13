package Debian::Control::Stanza;

use strict;
use warnings;

use Carp qw(croak);

our $AUTOLOAD;

use overload '""' => \&as_string;

sub fields {
    return ();
}

sub new {
    my ( $class, $init ) = @_;
    $init ||= {};

    my $self = bless { _values => {}, _order => [] }, $class;

    while ( my ( $field, $value ) = each %{$init} ) {
        ( my $normalized = $field ) =~ s/-/_/g;
        croak "Invalid field given ($normalized)"
            unless $class->_is_valid_field($normalized);
        $self->set( $normalized, $value );
    }

    $self->Reorder( map { _canonical_field($_) } $class->fields );

    return $self;
}

sub _is_valid_field {
    my ( $class, $field ) = @_;
    my %fields = map { $_ => 1 } $class->fields;
    return exists $fields{$field};
}

sub _canonical_field {
    my ($field) = @_;
    $field =~ s/_/-/g;
    return $field;
}

sub is_dependency_list {
    my ( $self, $field ) = @_;
    $field =~ s/_/-/g;

    my %fields = map { $_ => 1 } qw(
      Build-Depends
      Build-Depends-Indep
      Build-Conflicts
      Build-Conflicts-Indep
      Depends
      Conflicts
      Enhances
      Replaces
      Breaks
      Pre-Depends
      Recommends
      Suggests
    );

    return exists $fields{$field};
}

sub is_comma_separated {
    my ( $self, $field ) = @_;
    $field =~ s/_/-/g;

    return 1 if $self->is_dependency_list($field);
    return $field eq 'Uploaders' || $field eq 'Provides';
}

sub get {
    my ( $self, $field ) = @_;
    $field = _canonical_field($field);
    return $self->{_values}{$field};
}

sub set {
    my ( $self, $field, $value ) = @_;
    $field = _canonical_field($field);
    $value =~ s/\n\z// if defined $value;

    if ( !exists $self->{_values}{$field} ) {
        push @{ $self->{_order} }, $field;
    }
    $self->{_values}{$field} = $value;

    return $value;
}

sub FETCH {
    my ( $self, $field ) = @_;
    return $self->get($field);
}

sub STORE {
    my ( $self, $field, $value ) = @_;
    return $self->set( $field, $value );
}

sub Keys {
    my ( $self, $index ) = @_;
    return defined $index ? $self->{_order}[$index] : @{ $self->{_order} };
}

sub Values {
    my ( $self, $index ) = @_;
    my @values = map { $self->{_values}{$_} } @{ $self->{_order} };
    return defined $index ? $values[$index] : @values;
}

sub Reorder {
    my ( $self, @order ) = @_;
    my %wanted = map { $_ => 1 } @order;

    my @ordered = grep { exists $self->{_values}{$_} } @order;
    push @ordered, grep { !$wanted{$_} } @{ $self->{_order} };

    $self->{_order} = \@ordered;
    return;
}

sub sort_dependency_fields {
    my $self = shift;

    for my $field ( @{ $self->{_order} } ) {
        next unless $self->is_dependency_list($field);

        my $value = $self->{_values}{$field};
        next unless defined $value && $value ne '';

        my @items = map {
            my $item = $_;
            $item =~ s/^\s+//;
            $item =~ s/\s+$//;
            $item;
        } grep { $_ ne '' } split( /\s*,\s*/, $value );

        $self->{_values}{$field} = join( ', ', sort @items );
    }

    return;
}

sub as_string {
    my $self = shift;

    my @lines;
    for my $field ( map { _canonical_field($_) } $self->fields ) {
        next if $field =~ /^-/;
        next unless exists $self->{_values}{$field};

        my $value = $self->{_values}{$field};
        next unless defined $value;
        next if $self->is_dependency_list($field) && $value eq '';
        next if $self->is_comma_separated($field) && $value eq '';

        my @parts = split( /\n/, $value, -1 );
        my $first = shift @parts;
        push @lines, "$field: $first";
        push @lines, @parts;
    }

    return join( "\n", @lines ) . "\n";
}

sub AUTOLOAD {
    my $self = shift;
    ( my $field = $AUTOLOAD ) =~ s/.*:://;
    return if $field eq 'DESTROY';

    croak "Invalid field given ($field)"
        unless ref($self)->_is_valid_field($field);

    return @_ ? $self->set( $field, shift ) : $self->get($field);
}

1;
