SHELL := /bin/bash

# Set the C++ compiler
CXX = mpic++

# Set the compiler flags
CXXFLAGS = -std=c++11 -Wall -Wextra -pedantic -Werror -g

all: hello_world

hello_world: hello_world.cc
	@if ! command -v $(CXX) &> /dev/null; then \
		echo "Error: $(CXX) not found. Please load an appropriate MPI module (e.g. OpenMPI or MPICH)." >&2; \
		exit 1; \
	fi
	@echo "Compiling hello_world..."
	$(CXX) $(CXXFLAGS) -o hello_world hello_world.cc
	@echo "Done."

clean:
	@echo "Cleaning up..."
	rm hello_world
	@echo "Done."