import math
import os
import time # CPUの時間を計測
import numpy as np
import pycuda.gpuarray as gpuarray
import pycuda.driver as drv # GPUの時間を計測
from pycuda.compiler import SourceModule

# GPUの初期化
import pycuda.autoinit

# コンパイル時に余計なメッセージを表示させないようにする
os.environ["CL"] = r'-Xcompiler "/wd 4819'


# CUDA Cカーネルファイルの参照先の絶対パスを得る
cuda_file_path = os.path.abspath("./cuda")
#
#  CUDAカーネルの定義
#
module = SourceModule("""
#include "kernel_functions_for_math_1d.cu"
""", include_dirs=[cuda_file_path])

# コンパイルしたコードからカーネルを得る
plus_one_kernel = module.get_function("plus_one_kernel")

# 計算対象のnumpyアレーの作成
num_components = np.int32(1e5)
x = np.arange(num_components, dtype=np.int32)

#
#  cpuでの実行
#
time_start_cpu = time.time() # time.time()は実行された時点での時刻を記録する
x = x + 1
time_end_cpu = time.time() # time.time()は実行された時点での時刻を返す
# time.time()を実行する前と後で時刻を取得し、その差を計算することで実行時間を計測することができる。



#
#  gpuでの実行
#

# cpu to gpuへデータを送付
x_gpu = gpuarray.to_gpu(x) # gpuarray.to_gpu()はnumpyアレーをGPUメモリにコピーする
y_gpu = gpuarray.zeros(num_components, dtype=np.int32) # gpuarray.zeros()はGPUメモリに0で初期化されたnumpyアレーを作成する

# ブロック、グリッドの決定
threads_per_block = (256, 1, 1) # スレッド数は256
blocks_per_grid = (math.ceil(num_components / threads_per_block[0]), 1, 1) # ブロック数はnum_componentsをスレッド数で割った値の切り上げ

# 計測用イベント変数の用意
time_start_gpu = drv.Event()
time_end_gpu = drv.Event()

time_start_gpu2 = drv.Event()
time_end_gpu2 = drv.Event()

# CUDAカーネルの実行時間計測
time_start_gpu.record() # record()でフラグを立てる
# CUDAカーネルの実行
plus_one_kernel(num_components, y_gpu, x_gpu, block=threads_per_block, grid=blocks_per_grid) # 計測したい処理
time_end_gpu.record() # record()でフラグを立てる
time_end_gpu.synchronize() # CUDAカーネルの同期をとる

time_start_gpu2.record()
# gpu to cpuへデータを送付
y = y_gpu.get()
time_end_gpu2.record()
time_end_gpu2.synchronize()
#
# 実行時間の比較
#
print("CPU calculation {0} [msec]".format(1000 * (time_end_cpu - time_start_cpu))) # 1000をかけることで単位をミリ秒に変換
gpu_exec = time_start_gpu.time_till(time_end_gpu) + time_start_gpu.time_till(time_end_gpu2) # time_till()はイベント変数の時刻の差を返す
print("GPU calculation {0} [msec]".format(gpu_exec))
print("kernel exec {0} [msec]".format(time_start_gpu.time_till(time_end_gpu)))
print("memory copy {0} [msec]".format(time_start_gpu.time_till(time_end_gpu2)))


print("x :", x)
print("y :", y)
