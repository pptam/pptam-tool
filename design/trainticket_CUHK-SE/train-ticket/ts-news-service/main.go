package main

import (
	"context"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/stdout/stdouttrace"
	"go.opentelemetry.io/otel/sdk/resource"
	"go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.24.0"
)

type News struct {
	Title   string `json:"Title"`
	Content string `json:"Content"`
}

func initTracer() {
	exporter, err := stdouttrace.New(stdouttrace.WithPrettyPrint())
	if err != nil {
		log.Fatalf("Failed to create stdout trace exporter: %v", err)
	}

	res, err := resource.New(context.Background(),
		resource.WithAttributes(
			semconv.ServiceNameKey.String("ExampleService"),
		),
	)
	if err != nil {
		log.Fatalf("Failed to create resource: %v", err)
	}

	tp := trace.NewTracerProvider(
		trace.WithBatcher(exporter),
		trace.WithResource(res),
	)
	otel.SetTracerProvider(tp)
}

func traceMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		tracer := otel.Tracer("gin-server")
		ctx, span := tracer.Start(c.Request.Context(), "Handle "+c.Request.Method+" "+c.Request.URL.Path)
		defer span.End()

		c.Request = c.Request.WithContext(ctx)
		c.Next()
	}
}

func main() {
	initTracer()
	r := gin.Default()
	r.Use(traceMiddleware())

	r.GET("/hello", func(c *gin.Context) {
		c.String(200, "Hello, World!")
	})

	r.GET("/news-service/news", func(c *gin.Context) {
		newsList := []News{
			{Title: "News Title 1", Content: "News Content 1"},
			{Title: "News Title 2", Content: "News Content 2"},
		}
		c.JSON(http.StatusOK, newsList)
	})

	r.Run()
}
