from umqtt.simple import MQTTClient
import sys
import machine

class Mqtt():
    def __init__(self, parent, settings):
        print("Initializing MQTT Client")
        self.settings = settings
        self.parent = parent

        self.timer = machine.Timer(self.settings["timer_id"])

        self.mqtt = MQTTClient(self.settings["client_name"], self.settings["server_ip"], self.settings["server_port"])
        self.mqtt.set_callback(self.receive_msgs)

    def connect(self, event = None):
        try:
            self.mqtt.connect()
        except Exception as e:
            print("Error wile connecting to the mqtt server")
            sys.print_exception(e)
            
        self.mqtt.subscribe("kolava/"+self.settings["client_name"]+"/#")
        self.timer.init(mode=machine.Timer.PERIODIC, period=self.settings["subscription_poll_time"], callback=self.timer_callback)

        print("Connected to the mqtt server")
        self.parent.call_callbacks("mqtt_on_connect_callback")

    def timer_callback(self, timer):
        self.mqtt.check_msg()

    def publish(self,topic,msg,retain=False,qos=0):
        if hasattr(self.parent, "wifi") and self.parent.wifi.nic.isconnected():
            self.mqtt.publish(topic,str(msg),retain,qos)

    def receive_msgs(self,topic,msg):
        topic = topic.decode('utf-8').split("/")
        msg= msg.decode('utf-8')
        print("MQTT message received: {}: {}".format(topic, msg))
        self.parent.call_callbacks("mqtt_on_message_received",topic=topic[2],msg=msg)
    
    def mqtt_on_connect_callback(self,**kwargs):
        self.publish("kolava/node_online", self.settings["client_name"])

    def wifi_on_connect_callback(self,**kwargs):
        self.connect()