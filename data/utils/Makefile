CXX ?= g++
CC ?= gcc
CFLAGS = -Wall -Wconversion -O3 -fPIC

all: scale

scale: scale.cpp
	$(CXX) $(CFLAGS) -o scale scale.cpp

clean:
	rm -rf scale
