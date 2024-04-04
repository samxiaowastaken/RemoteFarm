import adafruit_dht
import board

class DHTHandler:
    """
    一个用于处理DHT传感器操作的类。

    ...

    属性
    ----------
    dht_devices : dict
        存储传感器ID和对应的DHT设备的字典

    方法
    -------
    read_dht_data(id):
        读取指定ID的DHT传感器的温度和湿度数据。
    """

    def __init__(self):
        """
        构造DHTHandler对象所需的所有必要属性。

        ...

        属性
        ----------
        dht_devices : dict
            存储传感器ID和对应的DHT设备的字典
        """
        self.sensor_dict = {}
        # 传感器ID和对应的DHT设备地址的字典
        # 例子：sensor_dict = {1: board.D4, 2: board.D5}

        for id, pin in self.sensor_dict.items():
            self.dht_devices[id] = adafruit_dht.DHT22(pin)

    def read_dht_data(self, id):
        """
        读取指定ID的DHT传感器的温度和湿度数据。
        """
        dht_device = self.dht_devices.get(id)
        if dht_device is None:
            print(f"无法找到ID为{id}的DHT传感器")
            return None, None

        try:
            # 读取温湿度
            temperature_c = dht_device.temperature
            humidity = dht_device.humidity
            # 返回一个元组，包含温度和湿度值
            return temperature_c, humidity
        except RuntimeError as error:
            # 错误处理，如无法读取数据时返回None
            print(f"无法读取DHT传感器数据: {error}")
            return None, None