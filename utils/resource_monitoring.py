import psutil
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

import psutil
import os

class ResourceMonitoring:
    @staticmethod
    def log_memory_usage():
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        total_memory = psutil.virtual_memory().total
        rss_percent = mem_info.rss / total_memory * 100
        vms_percent = mem_info.vms / total_memory * 100
        print(f"Memory usage: \n RSS={mem_info.rss / (1024 ** 2):.2f} MB ({rss_percent:.2f}%), \n VMS={mem_info.vms / (1024 ** 2):.2f} MB ({vms_percent:.2f}%)")

    @staticmethod
    def monitor_memory_usage(rss_threshold=80, vms_threshold=200):
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        total_memory = psutil.virtual_memory().total
        rss_percent = mem_info.rss / total_memory * 100
        vms_percent = mem_info.vms / total_memory * 100
        return rss_percent < rss_threshold and vms_percent < vms_threshold

    @staticmethod
    def get_memory_usage():
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        total_memory = psutil.virtual_memory().total
        rss_percent = mem_info.rss / total_memory * 100
        vms_percent = mem_info.vms / total_memory * 100
        rss_mb = mem_info.rss / (1024 ** 2)
        vms_mb = mem_info.vms / (1024 ** 2)
        return rss_percent, vms_percent, rss_mb, vms_mb