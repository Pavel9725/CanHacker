from app.can_row import CANRow


class CANModel:
    def __init__(self):
        self.rows = {}

    def handle_frame(self, frame):
        row = self.rows.get(frame.can_id)

        if row is None:
            self.rows[frame.can_id] = CANRow(frame)
            return

        row.update(frame)


    def get_row(self, can_id):
        return self.rows.get(can_id)


    def get_all(self):
        return list(self.rows.values())


    def get_ids(self):
        return list(self.rows.keys())

    def __len__(self):
        return len(self.rows)


    def get_data(self, can_id):
        row = self.get_row(can_id)

        if row is None:
            return None

        return row.get_data()


    def get_changed_bytes(self, can_id):
        row = self.get_row(can_id)

        if row is None:
            return []

        return row.get_changed_bytes()

