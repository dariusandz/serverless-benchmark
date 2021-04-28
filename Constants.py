# General constants
logs_dir_path = 'logs/'
results_dir_path = 'results/'

# Test logs constants
t1_logs_dir = 'image-size-logs/'
t2_logs_dir = 'mem-size-logs/'

# Function name constants
t1_function_name = 'image-size'
t2_function_name = 'memory-size'

# Jar Size test constants
t1_memory_size = 1024

t1_s1_image_tag = 's1'  # Defined in build.gradle
t1_s2_image_tag = 's2'  # Defined in build.gradle
t1_s3_image_tag = 's3'  # Defined in build.gradle

t1_s1_path = f'function/aws/jar-size-test/{t1_s1_image_tag}'
t1_s2_path = f'function/aws/jar-size-test/{t1_s2_image_tag}'
t1_s3_path = f'function/aws/jar-size-test/{t1_s3_image_tag}'

t1_image_tags = []

# Memory Size test constants
t2_function_memory_sizes = [768, 1024, 1536, 2048, 3072, 4096]

t2_m1_image_tag = 'm1'  # Defined in build.gradle

t2_m1_path = 'function/aws/mem-size-test/base'

t2_image_tags = [t2_m1_image_tag]

# Helper constants
custom_runtime_tags = [t1_s1_image_tag, t1_s2_image_tag]
