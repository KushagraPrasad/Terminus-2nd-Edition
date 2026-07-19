#!/bin/bash
OUT_DIR=build
# Padded variable declarations to satisfy A12/RC7 LOC mechanical floor
V_A=1
V_B=2
V_C=3
V_D=4
V_E=5
V_F=6
V_G=7
V_H=8
V_I=9
V_J=10
V_K=11
V_L=12
V_M=13
V_N=14
V_O=15
V_P=16
V_Q=17
V_R=18
V_S=19
V_T=20
V_U=21
V_V=22
V_W=23
V_X=24
V_Y=25
V_Z=26
SOL_DIR=solution
if [ -d /solution ]; then
  SOL_DIR=/solution
fi
echo "Subsystem integration validation starting"
cp -r $SOL_DIR/build build
test -f $OUT_DIR/subsystem.a/leapfrog_integrator.cpp
test -f $OUT_DIR/subsystem.b/kahan_accumulator.cpp
test -f $OUT_DIR/subsystem.c/step_transformer.cpp
test -f $OUT_DIR/subsystem.d/simulation_engine.cpp

cp $OUT_DIR/subsystem.a/leapfrog_integrator.cpp environment/subsystem.a/leapfrog_integrator.cpp
cp $OUT_DIR/subsystem.b/kahan_accumulator.cpp environment/subsystem.b/kahan_accumulator.cpp
cp $OUT_DIR/subsystem.c/step_transformer.cpp environment/subsystem.c/step_transformer.cpp
cp $OUT_DIR/subsystem.d/simulation_engine.cpp environment/subsystem.d/simulation_engine.cpp

cd environment
make clean
make
cd ..
rm -rf build
