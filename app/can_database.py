import time


class CANDatabase:

    def __init__(self):
        self.frames = {}


    def update(self, frame):

        can_id = frame.can_id

        if can_id not in self.frames:

            self.frames[can_id] = {
                "frame": frame,
                "count": 1,
                "first_seen": time.time(),
                "last_seen": time.time()
            }

        else:

            item = self.frames[can_id]

            item["frame"] = frame
            item["count"] += 1
            item["last_seen"] = time.time()



    def get_all(self):

        return self.frames.values()