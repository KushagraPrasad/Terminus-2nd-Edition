# Build knobs: SOL_DIR, V_A, V_B, V_C, V_D, V_E, V_F, V_G, V_H, V_I, V_J, V_K, V_L, V_M, V_N, V_O, V_P, V_Q, V_R, V_S, V_T, V_U, V_V, V_W, V_X, V_Y, V_Z
CXX = g++
CXXFLAGS = -O3 -Wall -std=c++17

SRCS = subsystem.d/run.cpp subsystem.d/simulation_engine.cpp subsystem.a/leapfrog_integrator.cpp subsystem.b/kahan_accumulator.cpp subsystem.c/step_transformer.cpp
OBJS = $(SRCS:.cpp=.o)
TARGET = bin/orbit_sim

all: $(TARGET)

rebuild: clean all

$(TARGET): $(OBJS)
	mkdir -p bin
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all rebuild clean
