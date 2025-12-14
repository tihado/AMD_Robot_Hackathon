import torch

print(torch.cuda.is_initialized())
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.current_device())
print(torch.cuda.get_device_capability(0))
print(torch.cuda.get_device_properties(0))

print(torch.cuda.memory.mem_get_info(0))
print(torch.cuda.memory_summary(0))
print(torch.cuda.memory.memory_allocated(0))