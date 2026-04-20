from functools import wraps
from typing import Callable
from live_chrono import LiveChrono  # 核心依赖


def timed_task(label=None) -> Callable:
    """
    无多线程版本实时计时器装饰器
    使用 live_chrono 实现，自动清理控制台行，支持自定义标签
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # 初始化实时计时器
            if label is not None:
                chrono = LiveChrono(display_format=f"[{label}] Elapsed: %H:%M:%S")
            else:
                chrono = LiveChrono(display_format=f"Elapsed: %H:%M:%S")
            
            # 启动计时 + 自定义显示格式
            if label:
                # 带标签格式
                chrono.start()
            else:
                # 无标签格式
                chrono.start()

            try:
                # 执行目标函数
                return func(*args, **kwargs)
            finally:
                # 停止计时 + 自动清空控制台行（live_chrono 原生支持）
                chrono.stop()

        return wrapper

    # 支持两种用法：@timed_task 和 @timed_task(label="xxx")
    if callable(label):
        func = label
        label = None
        return decorator(func)

    return decorator
