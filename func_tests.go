package shapes

import (
	"math"
	"testing"
)

func TestCircle(t *testing.T) {
	c := Circle{Radius: 5}
	gotPerimeter := c.Perimeter()
	wantPerimeter := 2 * math.Pi * 5
	if math.Abs(gotPerimeter-wantPerimeter) > 0.001 {
		t.Errorf("Perimeter() = %.4f, want %.4f", gotPerimeter, wantPerimeter)
	}

	gotArea := c.Area()
	wantArea := math.Pi * 25
	if math.Abs(gotArea-wantArea) > 0.001 {
		t.Errorf("Area() = %.4f, want %.4f", gotArea, wantArea)
	}
}

func TestTriangle(t *testing.T) {
	tri := Triangle{A: 3, B: 4, C: 5}
	
	gotPerimeter := tri.Perimeter()
	wantPerimeter := 12.0
	if gotPerimeter != wantPerimeter {
		t.Errorf("Perimeter() = %.2f, want %.2f", gotPerimeter, wantPerimeter)
	}

	gotArea := tri.Area()
	wantArea := 6.0
	if math.Abs(gotArea-wantArea) > 0.001 {
		t.Errorf("Area() = %.4f, want %.4f", gotArea, wantArea)
	}
}

func TestRectangle(t *testing.T) {
	rect := Rectangle{Width: 6, Height: 4}
	
	gotPerimeter := rect.Perimeter()
	wantPerimeter := 20.0
	if gotPerimeter != wantPerimeter {
		t.Errorf("Perimeter() = %.2f, want %.2f", gotPerimeter, wantPerimeter)
	}

	gotArea := rect.Area()
	wantArea := 24.0
	if gotArea != wantArea {
		t.Errorf("Area() = %.2f, want %.2f", gotArea, wantArea)
	}
}

func TestSquare(t *testing.T) {
	square := Rectangle{Width: 5, Height: 5}
	
	gotPerimeter := square.Perimeter()
	wantPerimeter := 20.0
	if gotPerimeter != wantPerimeter {
		t.Errorf("Perimeter() = %.2f, want %.2f", gotPerimeter, wantPerimeter)
	}

	gotArea := square.Area()
	wantArea := 25.0
	if gotArea != wantArea {
		t.Errorf("Area() = %.2f, want %.2f", gotArea, wantArea)
	}
}

func BenchmarkCircleArea(b *testing.B) {
	c := Circle{Radius: 10}
	for i := 0; i < b.N; i++ {
		c.Area()
	}
}

func BenchmarkTriangleArea(b *testing.B) {
	tri := Triangle{A: 3, B: 4, C: 5}
	for i := 0; i < b.N; i++ {
		tri.Area()
	}
}