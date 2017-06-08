class RecordingDevice:
    """
    Prototype for different kinds of recording devices
    """
    def __init__(self):
        self.schedule = []
        self.active = False
        self.message_text = ''