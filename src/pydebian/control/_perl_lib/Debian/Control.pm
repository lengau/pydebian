package Debian::Control;

use strict;
use warnings;

use Debian::Control::Stanza::Binary;
use Debian::Control::Stanza::Source;

sub new {
    my $class = shift;

    my %binary;
    my $self = bless {
        source => Debian::Control::Stanza::Source->new(),
        binary => \%binary,
    }, $class;
    $self->{binary_tie} = Debian::Control::BinaryTie->new( $self->{binary} );

    return $self;
}

sub source {
    my $self = shift;
    $self->{source} = shift if @_;
    return $self->{source};
}

sub binary {
    my $self = shift;
    $self->{binary} = shift if @_;
    return $self->{binary};
}

sub binary_tie {
    my $self = shift;
    $self->{binary_tie} = shift if @_;
    return $self->{binary_tie};
}

sub read {
    my ( $self, $file ) = @_;

    my $content;
    if ( ref($file) and ref($file) eq 'SCALAR' ) {
        $content = $$file;
    }
    elsif ( ref($file) and ref($file) eq 'GLOB' ) {
        local $/;
        $content = <$file>;
    }
    else {
        open my $fh, '<', $file or die "Unable to open '$file' for reading: $!";
        local $/;
        $content = <$fh>;
        close $fh;
    }

    my %binary;
    $self->binary( \%binary );
    $self->binary_tie( Debian::Control::BinaryTie->new( $self->binary ) );
    $self->source( Debian::Control::Stanza::Source->new() );

    for my $paragraph ( grep { /\S/ } split( /\n(?:[ \t]*\n)+/, $content ) ) {
        my $data = _parse_paragraph($paragraph);
        if ( exists $data->{Source} ) {
            $self->source( Debian::Control::Stanza::Source->new($data) );
        }
        elsif ( exists $data->{Package} ) {
            my $binary = Debian::Control::Stanza::Binary->new($data);
            $self->binary_tie->Push( $data->{Package}, $binary );
        }
        else {
            die "Got control stanza with neither Source nor Package field\n";
        }
    }

    return;
}

sub _parse_paragraph {
    my ($paragraph) = @_;

    my %data;
    my $current;

    for my $line ( split( /\n/, $paragraph, -1 ) ) {
        next if $line eq '';

        if ( $line =~ /^([A-Za-z0-9][-A-Za-z0-9]*):\s*(.*)$/ ) {
            $current = $1;
            $data{$current} = $2;
            next;
        }

        if ( $line =~ /^[ \t]/ ) {
            die "Continuation line without a field\n" unless defined $current;
            $data{$current} .= "\n$line";
            next;
        }

        die "Unable to parse line '$line'\n";
    }

    return \%data;
}

sub write {
    my ( $self, $file ) = @_;

    for my $stanza ( $self->source, $self->binary_tie->Values ) {
        $stanza->sort_dependency_fields;
    }

    my $content = join( "\n", $self->source, $self->binary_tie->Values );

    if ( ref($file) and ref($file) eq 'SCALAR' ) {
        $$file = $content;
    }
    elsif ( ref($file) and ref($file) eq 'GLOB' ) {
        print {$file} $content;
    }
    else {
        open my $fh, '>', $file or die "Unable to open '$file' for writing: $!";
        print {$fh} $content;
        close $fh;
    }

    return;
}

sub is_arch_dep {
    my $self = shift;

    my $binary = $self->binary_tie->Values(0);
    return undef unless defined $binary;

    my $architecture = $binary->Architecture;
    return undef unless defined $architecture;

    return $architecture ne 'all';
}

package Debian::Control::BinaryTie;

use strict;
use warnings;

sub new {
    my ( $class, $binary ) = @_;
    return bless { binary => $binary, order => [] }, $class;
}

sub Push {
    my ( $self, $key, $value ) = @_;
    push @{ $self->{order} }, $key unless exists $self->{binary}{$key};
    $self->{binary}{$key} = $value;
    return;
}

sub Keys {
    my ( $self, $index ) = @_;
    return defined $index ? $self->{order}[$index] : @{ $self->{order} };
}

sub Values {
    my ( $self, $index ) = @_;
    my @values = map { $self->{binary}{$_} } @{ $self->{order} };
    return defined $index ? $values[$index] : @values;
}

1;
