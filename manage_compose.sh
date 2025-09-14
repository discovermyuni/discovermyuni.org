#!/bin/bash

# Docker Compose Development Scripts
# Converted from justfile for bash compatibility
#
# Just does not yet manage signals for subprocesses reliably, which can lead to unexpected behavior.
# Exercise caution before expanding its usage in production environments.
# For more information, see https://github.com/casey/just/issues/2473 .

export COMPOSE_FILE="docker-compose.yml"

# Function to display help/usage information
show_help() {
    echo "Available commands:"
    echo "  build           - Build python image"
    echo "  up              - Start up containers"
    echo "  down            - Stop containers"
    echo "  restart         - Restart containers"
    echo "  prune           - Remove containers and their volumes"
    echo "  logs            - View container logs"
    echo "  seed            - Seed sample data"
    echo "  manage          - Execute manage.py commands"
    echo "  help            - Show this help message"
    echo ""
    echo "Usage examples:"
    echo "  $0 build"
    echo "  $0 up"
    echo "  $0 down"
    echo "  $0 restart"
    echo "  $0 prune --volumes"
    echo "  $0 logs django"
    echo "  $0 seed [--mode clear]"
    echo "  $0 manage migrate"
    echo "  $0 manage createsuperuser"
}

# Function to build python image
build() {
    echo "Building python image..."
    docker compose -f "$COMPOSE_FILE" build
}

# Function to start up containers
up() {
    echo "Starting up containers..."
    docker compose -f "$COMPOSE_FILE" up -d --remove-orphans
}

# Function to stop containers
down() {
    echo "Stopping containers..."
    docker compose -f "$COMPOSE_FILE" down
}

# Function to restart containers
restart() {
    echo "Restarting containers..."
    docker compose -f "$COMPOSE_FILE" restart "$@"
}

# Function to remove containers and their volumes
prune() {
    echo "Killing containers and removing volumes..."
    docker compose -f "$COMPOSE_FILE" down -v "$@"
}

# Function to view container logs
logs() {
    docker compose -f "$COMPOSE_FILE" logs -f "$@"
}

seed() {
    docker compose -f "$COMPOSE_FILE" exec django python3 ./manage.py seed "$@"
}

# Function to execute manage.py commands
manage() {
    if [ $# -eq 0 ]; then
        echo "Error: manage command requires arguments"
        echo "Usage: $0 manage <django_command> [args...]"
        echo "Example: $0 manage migrate"
        return 1
    fi
    docker compose -f "$COMPOSE_FILE" run --rm django python ./manage.py "$@"
}



# Main script logic
case "${1:-help}" in
    build)
        build
        ;;
    up)
        up
        ;;
    down)
        down
        ;;
    restart)
        shift  # Remove 'restart' from arguments
        restart "$@"
        ;;
    prune)
        shift  # Remove 'prune' from arguments
        prune "$@"
        ;;
    logs)
        shift  # Remove 'logs' from arguments
        logs "$@"
        ;;
    seed)
        shift  # Remove 'seed' from arguments
        seed "$@"
        ;;
    manage)
        shift  # Remove 'manage' from arguments
        manage "$@"
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo "Error: Unknown command '$1'"
        echo ""
        show_help
        exit 1
        ;;
esac
