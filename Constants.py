import numpy as np

# General constants
logs_dir_path = 'logs/'
results_dir_path = 'results/'

ecr_repository_name = 'lambda-benchmark'
s3_bucket_name = 'serverless-benchmark'

mem_per_1vCPU = 1769

# Test logs constants
t1_logs_dir = 'image-size-logs/'
t2_logs_dir = 'mem-size-logs/'
t3_logs_dir = 'zip-package-logs/'

# Function name constants
t1_function_name = 'image-size'
t2_function_name = 'memory-size'
t3_function_name = 'zip-package'

# Jar Size test constants
t1_memory_size = 4096

t1_s1_image_tag = 's1'  # Defined in build.gradle
t1_s2_image_tag = 's2'  # Defined in build.gradle
t1_s3_image_tag = 's3'  # Defined in build.gradle

t1_s1_path = f'function/aws/jar-size-test/{t1_s1_image_tag}'
t1_s2_path = f'function/aws/jar-size-test/{t1_s2_image_tag}'
t1_s3_path = f'function/aws/jar-size-test/{t1_s3_image_tag}'

t1_image_tags = []

# Memory Size test constants
t2_function_memory_sizes_0 = np.array([256, 512, 768, 1024])
t2_function_memory_sizes_1 = np.array([2654, 4422, 6191, 7960, 9729])
t2_function_memory_sizes_2 = np.array([1769, 3538, 5307, 7076, 8845, 10240])

t2_m1_image_tag = 'm1'  # Defined in build.gradle

t2_m1_path = 'function/aws/mem-size-test/base'

t2_image_tags = [t2_m1_image_tag]

# Zip package test constants
t3_memory_size = 1024

t3_z1_tag = 'z1'
t3_z2_tag = 'z2'
t3_z3_tag = 'z3'

t3_z1_path = f'function/aws/zip-package-test/{t3_z1_tag}'
t3_z2_path = f'function/aws/zip-package-test/{t3_z2_tag}'
t3_z3_path = f'function/aws/zip-package-test/{t3_z3_tag}'
t3_z3_path_function = f'function/aws/zip-package-test/{t3_z3_tag}/function'
t3_z3_path_runtime = f'function/aws/zip-package-test/{t3_z3_tag}/runtime'

t3_z3_runtime_layer_name = 'lambda-runtime'

# Helper constants
custom_runtime_tags = [t1_s1_image_tag, t1_s2_image_tag, t2_m1_image_tag]
providable_runtime_layer_tags = [t3_z2_tag, t3_z3_tag]
