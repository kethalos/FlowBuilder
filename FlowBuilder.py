import tkinter as tk
import winsound
#test
# ---------------------- CONFIG ----------------------
MAX_WORK_MINUTES = 25
MAX_BREAK_MINUTES = 10

def minutes_to_seconds(m):
    return m * 60

def seconds_to_hms(seconds):
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}"

# ---------------------- APP ----------------------
class FlowBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("FlowBuilder")
        self.root.geometry("400x500")

        self.default_work = 5 * 60
        self.default_break = 5 * 60
        self.current_work = self.default_work
        self.current_break = self.default_break
        self.total_required_seconds = 8 * 3600  # 8 hours default
        self.time_completed = 0

        self.is_work_session = True
        self.timer_running = False

        self.build_config_screen()

    def build_config_screen(self):
        self.clear_screen()
        self.root.configure(bg="green")

        tk.Label(self.root, text="Configure Your Session", font=("Helvetica", 16), bg="green", fg="white").pack(pady=10)

        self.work_var = tk.StringVar(value="5")
        self.break_var = tk.StringVar(value="5")
        self.goal_hours_var = tk.StringVar(value="8")
        self.goal_minutes_var = tk.StringVar(value="0")

        tk.Label(self.root, text="Work Timer (minutes):", bg="green", fg="white").pack()
        tk.OptionMenu(self.root, self.work_var, *[str(i) for i in range(1, 26)]).pack()

        tk.Label(self.root, text="Break Timer (minutes):", bg="green", fg="white").pack()
        tk.OptionMenu(self.root, self.break_var, *[str(i) for i in range(1, 11)]).pack()

        tk.Label(self.root, text="Daily Goal (hours & minutes):", bg="green", fg="white").pack()
        frame = tk.Frame(self.root, bg="green")
        frame.pack()
        tk.OptionMenu(frame, self.goal_hours_var, *[str(i) for i in range(0, 13)]).pack(side="left")
        tk.Label(frame, text="h", bg="green", fg="white").pack(side="left")
        tk.OptionMenu(frame, self.goal_minutes_var, *[str(i) for i in range(0, 60, 5)]).pack(side="left")
        tk.Label(frame, text="m", bg="green", fg="white").pack(side="left")

        tk.Button(self.root, text="Start Session", command=self.save_and_start, font=("Helvetica", 14)).pack(pady=20)

    def save_and_start(self):
        self.default_work = minutes_to_seconds(int(self.work_var.get()))
        self.default_break = minutes_to_seconds(int(self.break_var.get()))
        goal_hours = int(self.goal_hours_var.get())
        goal_minutes = int(self.goal_minutes_var.get())
        self.total_required_seconds = goal_hours * 3600 + goal_minutes * 60
        self.current_work = self.default_work
        self.current_break = self.default_break
        self.show_start_button()

    def show_start_button(self):
        self.clear_screen()
        self.root.configure(bg="green")
        self.remaining_label = tk.Label(self.root, text=f"Remaining Today: {seconds_to_hms(self.time_remaining())}", font=("Helvetica", 12), bg="green", fg="white")
        self.remaining_label.pack(pady=5)
        tk.Label(self.root, text=f"Next Timer: {self.current_work // 60} minutes\nPress Start to Begin.", font=("Helvetica", 14), bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Start Work Timer", command=self.start_work_timer, font=("Helvetica", 14)).pack(pady=10)

    def time_remaining(self):
        return max(0, self.total_required_seconds - self.time_completed)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_timer(self, duration, label, kind, on_complete):
        if duration > 0:
            mins, secs = divmod(duration, 60)
            label.config(text=f"{kind}\n{mins:02}:{secs:02}")
            self.remaining_label.config(text=f"Remaining Today: {seconds_to_hms(self.time_remaining())}")
            self.root.after(1000, self.start_timer, duration - 1, label, kind, on_complete)
        else:
            for _ in range(3):
                winsound.Beep(1000, 300)
            on_complete()

    def start_work_timer(self):
        self.is_work_session = True
        self.clear_screen()
        self.root.configure(bg="green")
        label = tk.Label(self.root, text="WORK", font=("Helvetica", 48, "bold"), bg="green", fg="white")
        label.pack(pady=30)
        self.remaining_label = tk.Label(self.root, text=f"Remaining Today: {seconds_to_hms(self.time_remaining())}", font=("Helvetica", 12), bg="green", fg="white")
        self.remaining_label.pack(pady=10)
        self.start_timer(self.current_work, label, "WORK", self.after_work)

    def after_work(self):
        self.time_completed += self.current_work
        self.show_continue_or_break()

    def show_continue_or_break(self):
        self.clear_screen()
        self.root.configure(bg="green")
        self.remaining_label = tk.Label(self.root, text=f"Remaining Today: {seconds_to_hms(self.time_remaining())}", font=("Helvetica", 12), bg="green", fg="white")
        self.remaining_label.pack(pady=10)
        tk.Label(self.root, text="Work Complete! Continue or Take a Break?", font=("Helvetica", 14), bg="green", fg="white").pack(pady=10)
        tk.Button(self.root, text="Continue", command=self.start_work_timer, font=("Helvetica", 14)).pack(pady=5)
        tk.Button(self.root, text="Take a Break", command=self.prompt_rating, font=("Helvetica", 14)).pack(pady=5)

    def prompt_rating(self):
        self.clear_screen()
        self.root.configure(bg="green")
        tk.Label(self.root, text="Rate your session:\n1: Distracted\n2: Okay\n3: Focused\n4: Flow State", font=("Helvetica", 14), bg="green", fg="white").pack(pady=10)
        self.rating_entry = tk.Entry(self.root, font=("Helvetica", 14))
        self.rating_entry.pack(pady=5)
        tk.Button(self.root, text="Submit Rating", command=self.submit_rating, font=("Helvetica", 14)).pack(pady=10)

    def submit_rating(self):
        try:
            rating = int(self.rating_entry.get())
            if rating == 1:
                self.current_work = max(60, self.current_work - 2 * 60)
            elif rating == 3:
                self.current_work = min(25 * 60, self.current_work + 2 * 60)
            elif rating == 4:
                self.current_work = min(25 * 60, self.current_work + 3 * 60)
        except ValueError:
            return  # Invalid input; ignore
        self.ask_custom_override()

    def ask_custom_override(self):
        self.clear_screen()
        self.root.configure(bg="blue")
        tk.Label(self.root, text="Adjust Timers? Or Use Recommended?", font=("Helvetica", 14), bg="blue", fg="white").pack(pady=10)

        self.override_work_var = tk.StringVar(value=str(self.current_work // 60))
        self.override_break_var = tk.StringVar(value=str(self.current_break // 60))

        tk.Label(self.root, text="New Work Time (min):", bg="blue", fg="white").pack()
        tk.OptionMenu(self.root, self.override_work_var, *[str(i) for i in range(1, 26)]).pack()
        tk.Label(self.root, text="New Break Time (min):", bg="blue", fg="white").pack()
        tk.OptionMenu(self.root, self.override_break_var, *[str(i) for i in range(1, 11)]).pack()

        def confirm_override():
            self.current_work = minutes_to_seconds(int(self.override_work_var.get()))
            self.current_break = minutes_to_seconds(int(self.override_break_var.get()))
            self.start_rest_timer()

        tk.Button(self.root, text="Confirm & Start Break", command=confirm_override, font=("Helvetica", 14)).pack(pady=10)

    def start_rest_timer(self):
        self.clear_screen()
        self.root.configure(bg="blue")
        label = tk.Label(self.root, text="REST", font=("Helvetica", 48, "bold"), bg="blue", fg="white")
        label.pack(pady=30)
        self.remaining_label = tk.Label(self.root, text=f"Remaining Today: {seconds_to_hms(self.time_remaining())}", font=("Helvetica", 12), bg="blue", fg="white")
        self.remaining_label.pack(pady=10)
        self.start_timer(self.current_break, label, "REST", self.show_start_button)


# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FlowBuilder(root)
    root.mainloop()
