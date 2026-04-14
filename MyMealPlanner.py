import tkinter as tk
from tkinter import messagebox
from db.meals import get_all_meals, add_meal, init_meals_db as init_meals, delete_meal, update_meal
from db.weeklyplan import add_to_plan, remove_from_plan, clear_entire_week, get_full_weekly_plan, remove_from_plan_by_name, get_plan_by_day, init_weekly_db as init_weekly # Umbenannt, um Konflikt zu vermeiden
from db.profile import init_profile_db as init_profile, get_profile, update_profile
import datetime

# Define standard fonts for a modern look
FONT_TITLE = ("Segoe UI", 16, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)

class MyMealPlanner(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        init_meals()
        init_weekly()
        init_profile()
        
        self.columnconfigure((0, 1), weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.current_meals = [] 

        # Frames
        self.frame_tl = tk.Frame(self, bg="#f0f0f0", bd=2, relief="groove")
        self.frame_tr = tk.Frame(self, bg="#f9f9f9", bd=2, relief="groove")
        self.frame_bl = tk.Frame(self, bg="#e0e0e0", bd=2, relief="groove")
        self.frame_br = tk.Frame(self, bg="#d0d0d0", bd=2, relief="groove")

        self.frame_tl.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_tr.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.frame_bl.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.frame_br.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)


        # --- TOP LEFT (Profile & Fitness) ---
        # loading data
        prof = get_profile()
        # ID, username, start_date, plan_name, daily_calories, current_weight, starting_weight, body_fat, deadlift, squat, run
        _, user, s_date, plan, d_cals, s_weight, c_weight, b_fat, dead, squat, run = prof

        start_dt = datetime.datetime.strptime(s_date, "%Y-%m-%d").date()
        days_since = (datetime.date.today() - start_dt).days
        achievement = (s_weight - c_weight) if plan.strip().lower() == "cut" else (c_weight - s_weight)

        # Settings Button
        self.btn_settings = tk.Button(
            self.frame_tl, text="⚙", font=("Segoe UI", 16), 
            bg="#f0f0f0", bd=0, fg="#555", cursor="hand2", command=self.edit_profile_dialog
        )
        self.btn_settings.place(relx=0.97, rely=0.03, anchor="ne")

        self.profile_center_frame = tk.Frame(self.frame_tl, bg="#f0f0f0")
        self.profile_center_frame.pack(expand=True)

        # 1. Welcome section
        self.lbl_welcome = tk.Label(
            self.profile_center_frame, text=f"Welcome back,\n{user}", 
            font=("Segoe UI", 18, "bold"), bg="#f0f0f0", fg="#333"
        )
        self.lbl_welcome.pack(pady=(0, 5))

        self.lbl_today = tk.Label(
            self.profile_center_frame, text=f"Today is {datetime.date.today().strftime('%A: %d.%m.%Y')}", 
            font=FONT_SMALL, bg="#f0f0f0", fg="#666"
        )
        self.lbl_today.pack()
 
        self.lbl_journey_days = tk.Label(
            self.profile_center_frame, text=f"It has been {days_since} days since we started this journey", 
            font=("Segoe UI", 9, "italic"), bg="#f0f0f0", fg="#888"
        )
        self.lbl_journey_days.pack(pady=(0, 15))

        # 2. Plan details
        plan_stats = (
            f"Current Plan: {plan}\n"
            f"Daily calorie requirement: {d_cals} kcal\n"
            f"Current Weight: {c_weight} kg\n"
            f"Achievement: {achievement:+.00001f} kg\n"
            f"Body Fat: {b_fat}%"
        )
        self.lbl_plan_details = tk.Label(
            self.profile_center_frame, text=plan_stats, font=FONT_NORMAL, 
            bg="#f0f0f0", justify="center"
        )
        self.lbl_plan_details.pack(pady=5)

        # 3. Divider
        self.profile_divider = tk.Label(
            self.profile_center_frame, text="------------------------------------------", 
            fg="#bbb", bg="#f0f0f0"
        )
        self.profile_divider.pack()

        # 4. Fitness Level
        self.lbl_fitness_title = tk.Label(
            self.profile_center_frame, text="Fitness Level", 
            font=("Segoe UI", 12, "bold"), bg="#f0f0f0", fg="#2196F3"
        )
        self.lbl_fitness_title.pack(pady=(0, 5))

        fitness_stats = (
            f"Max Deadlift: {dead} kg\n"
            f"Max Squat: {squat} kg\n"
            f"Longest Run: {run} km"
        )
        self.lbl_fitness_stats = tk.Label(
            self.profile_center_frame, text=fitness_stats, font=FONT_NORMAL, 
            bg="#f0f0f0", justify="center"
        )
        self.lbl_fitness_stats.pack()
    
        # --- BOTTOM LEFT ---
        self.frame_bl.grid_columnconfigure(0, weight=0)
        self.frame_bl.grid_columnconfigure(1, weight=0)
        self.frame_bl.grid_columnconfigure(2, weight=1)

        tk.Label(self.frame_bl, text="Add New Meal", font=FONT_TITLE, bg="#e0e0e0").grid(
            row=0, column=0, columnspan=2, pady=(20, 15), padx=(185, 0) # padx links schiebt es leicht ein
        )

        self.fields = ["Name", "Calories", "Proteins", "Carbs", "Fats", "Cost"]
        self.entries = {}

        for i, field in enumerate(self.fields):
            tk.Label(self.frame_bl, text=f"{field}:", font=FONT_NORMAL, bg="#e0e0e0").grid(
                row=i+1, column=0, padx=(125, 10), pady=5, sticky="e" # 50px Abstand vom linken Rand
            )
            entry = tk.Entry(self.frame_bl, font=FONT_NORMAL, width=25)
            entry.grid(row=i+1, column=1, padx=5, pady=5, sticky="w")
            self.entries[field] = entry

        # Recipe Multi-line
        tk.Label(self.frame_bl, text="Recipe:", font=FONT_NORMAL, bg="#e0e0e0").grid(
            row=7, column=0, padx=(125, 10), pady=5, sticky="ne"
        )
        self.recipe_text = tk.Text(self.frame_bl, font=FONT_NORMAL, width=25, height=5, wrap="word")
        self.recipe_text.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        # Save Button
        tk.Button(
            self.frame_bl, text="Save Meal", command=self.save_meal_to_db,
            bg="#4CAF50", fg="white", font=FONT_NORMAL, cursor="hand2", width=15
        ).grid(row=8, column=0, columnspan=2, pady=25, padx=(185, 0))

       
        tk.Label(self.frame_br, text="Meals", font=FONT_TITLE, bg="#d0d0d0").pack(pady=5)
        self.meal_listbox = tk.Listbox(self.frame_br, font=FONT_NORMAL, selectbackground="#4CAF50")
        self.meal_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.meal_listbox.bind("<Double-1>", self.on_double_click)
        self.meal_listbox.bind("<Button-3>", self.show_context_menu)
        self.setup_context_menu()
        self.refresh_meal_list()

        self.frame_tr.grid_columnconfigure(0, weight=1)
        self.frame_tr.grid_rowconfigure(1, weight=1) 

        tk.Label(self.frame_tr, text="Weekly Plan", font=FONT_TITLE, bg="#f9f9f9").grid(row=0, column=0, pady=10)

    
        self.canvas = tk.Canvas(self.frame_tr, bg="#f9f9f9", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.frame_tr, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f9f9f9")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=1, column=0, sticky="nsew", padx=(10, 0))
        self.scrollbar.grid(row=1, column=1, sticky="ns")

        self.summary_frame = tk.Frame(self.frame_tr, bg="#f9f9f9", bd=1, relief="sunken")
        self.summary_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        self.lbl_total_cals = tk.Label(self.summary_frame, text="Weekly Calories Total: 0", font=FONT_NORMAL, bg="#f9f9f9")
        self.lbl_total_cals.pack(anchor="w", padx=5)
        self.lbl_total_cost = tk.Label(self.summary_frame, text="Weekly Cost Total: 0.00 €", font=FONT_NORMAL, bg="#f9f9f9")
        self.lbl_total_cost.pack(anchor="w", padx=5)

        self.refresh_weekly_plan_ui()



        
    def edit_profile_dialog(self):
        prof = get_profile()
        top = tk.Toplevel(self)
        top.title("Edit Profile")
        top.geometry("350x500")
        top.configure(bg="#f0f0f0")

        fields = ["Name", "Plan", "Daily Calories", "Starting Weight", "Current Weight", "Body Fat", "Deadlift", "Squat", "Run"]

        # Index: 0=ID, 1=Name, 2=StartDate, 3=Plan, 4=Calories, 5=CurWeight, 6=StartWeight, 7=Fat, 8=Dead, 9=Squat, 10=Run
        db_indices = [1, 3, 4, 5, 6, 7, 8, 9, 10] 

        entries = {}

        for i, field in enumerate(fields):
            tk.Label(top, text=field, bg="#f0f0f0", font=FONT_SMALL).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            e = tk.Entry(top, font=FONT_SMALL)

            val = prof[db_indices[i]]

            e.insert(0, str(val) if val is not None else "")
            e.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entries[field] = e

        def save():
            try:
                n_name = entries["Name"].get()
                n_plan = entries["Plan"].get()
                n_curr_w = float(entries["Current Weight"].get())
                n_star_w = float(entries["Starting Weight"].get())
                n_b_fat = float(entries["Body Fat"].get())
                n_deadlift = float(entries["Deadlift"].get())
                n_squat =  float(entries["Squat"].get())
                n_run = float(entries["Run"].get())

                update_profile(n_name, n_plan, int(entries["Daily Calories"].get()), 
                               n_curr_w, n_star_w, float(entries["Body Fat"].get()), 
                               float(entries["Deadlift"].get()), float(entries["Squat"].get()), 
                               float(entries["Run"].get()))

                if n_star_w == n_curr_w:
                    achievement_display = "No Change"
                else:
                    if n_plan.strip().lower() == "cut":
                        new_achievement = n_star_w - n_curr_w
                    elif n_plan.strip().lower() == "bulk":
                        new_achievement = n_curr_w - n_star_w
                    else:
                        new_achievement = 0

                achievement_display = f"{new_achievement:+.1f} kg"

                updated_plan_text = (
                    f"Current Plan: {n_plan}\n"
                    f"Daily calorie requirement: {entries['Daily Calories'].get()} kcal\n"
                    f"Current Weight: {n_curr_w} kg\n"
                    f"Achievement: {achievement_display}\n" 
                    f"Body Fat: {n_b_fat}%"
                )

                updated_fitness_text = (
                    f"Max Deadlift: {n_deadlift} kg\n"
                    f"Max Squat: {n_squat} kg\n"
                    f"Longest Run: {n_run} km\n"
                )

                self.lbl_plan_details.config(text=updated_plan_text)
                self.lbl_fitness_stats.config(text=updated_fitness_text)
                top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Bitte nur Zahlen für Gewicht eingeben!")

        tk.Button(top, text="Save Changes", command=save, bg="#4CAF50", fg="white", font=FONT_NORMAL).grid(row=len(fields), columnspan=2, pady=20)

    def setup_context_menu(self):
        self.context_menu = tk.Menu(self, tearoff=0, font=FONT_NORMAL)
        
        # 2.1 Weekly Plan Cascade
        self.weekly_menu = tk.Menu(self.context_menu, tearoff=0, font=FONT_NORMAL)
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            self.weekly_menu.add_command(label=day, command=lambda d=day: self.add_to_weekly_plan(d))
            
        self.context_menu.add_cascade(label="Add to Weekly Plan", menu=self.weekly_menu)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Edit Meal", command=self.edit_meal)
        self.context_menu.add_command(label="Remove Meal", command=self.remove_meal)

    # --- CORE FUNCTIONS ---
    def save_meal_to_db(self):
        try:
            name = self.entries["Name"].get().strip()
            cals = int(self.entries["Calories"].get() or 0)
            prot = int(self.entries["Proteins"].get() or 0)
            carb = int(self.entries["Carbs"].get() or 0)
            fats = int(self.entries["Fats"].get() or 0)
            cost_input = self.entries["Cost"].get().strip().replace(',', '.')
            cost = float(cost_input) if cost_input else 0.0
            
            # Fetching from Text widget requires start and end positions
            recipe = self.recipe_text.get("1.0", tk.END).strip()

            if not name:
                raise ValueError("Name cannot be empty")

            add_meal(name, cals, prot, carb, fats, cost, recipe)
            
            # Clear all
            for entry in self.entries.values():
                entry.delete(0, tk.END)
            self.recipe_text.delete("1.0", tk.END)
                
            self.refresh_meal_list()
        except ValueError:
            messagebox.showerror("Input Error", "Please ensure macros and cost are numbers.")

    def refresh_meal_list(self):
        self.meal_listbox.delete(0, tk.END)
        self.current_meals = get_all_meals()
        
        for meal in self.current_meals:
            # Display format: Name - XXX kcal
            self.meal_listbox.insert(tk.END, f"{meal[1]} - {meal[2]} kcal")

    # --- INTERACTION FUNCTIONS ---
    def show_context_menu(self, event):
        # Force selection of the item under the cursor before opening menu
        index = self.meal_listbox.nearest(event.y)
        if index >= 0:
            self.meal_listbox.selection_clear(0, tk.END)
            self.meal_listbox.selection_set(index)
            self.meal_listbox.activate(index)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def on_double_click(self, event):
        selection = self.meal_listbox.curselection()
        if not selection: return
        
        # Meal tuple: (id, name, cal, prot, carb, fat, cost, recipe)
        meal = self.current_meals[selection[0]]
        name = meal[1]
        recipe = meal[7] if meal[7] else "No recipe added."

        # Create Recipe Window
        top = tk.Toplevel(self)
        top.title(f"Recipe View")
        top.geometry("400x300")
        top.configure(bg="#f9f9f9")

        tk.Label(top, text=name, font=FONT_TITLE, bg="#f9f9f9").pack(pady=10)
        tk.Label(top, text="Ingredients:", font=("Segoe UI", 12, "italic"), bg="#f9f9f9").pack(pady=5)
        
        recipe_text = tk.Text(top, font=FONT_NORMAL, wrap="word", bg="#f9f9f9", bd=0, height=10)
        recipe_text.pack(padx=20, pady=5, fill="both", expand=True)
        recipe_text.insert("1.0", recipe)
        recipe_text.config(state="disabled") # Make it read-only


    # --- CONTEXT MENU ACTIONS ---
    def refresh_weekly_plan_ui(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        from db.weeklyplan import get_plan_by_day, remove_from_plan

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # --- DATE ---
        today = datetime.date.today()
        monday_of_week = today - datetime.timedelta(days=today.weekday())

        # Cols: 0: Date, 1: Day, 2: Meal, 3: Calories, 4: Cost, 5: Action
        headers = ["Date", "  Day", "  Meal", "  Calories", "  Cost", ""]
        for col, text in enumerate(headers):
            tk.Label(
                self.scrollable_frame, 
                text=text, 
                font=("Segoe UI", 11, "bold"), 
                bg="#f9f9f9"
            ).grid(row=0, column=col, padx=15, pady=5, sticky="w")

        current_row = 1
        total_cals = 0
        total_cost = 0.0

        for i, day in enumerate(days):
            this_day_date = monday_of_week + datetime.timedelta(days=i)
            date_str = this_day_date.strftime("%d.%m.%Y")
            is_today = (this_day_date == today)

            row_font = ("Segoe UI", 10, "bold") if is_today else FONT_SMALL
            row_fg = "#000000" if not is_today else "#E91E63" 

            meals_for_day = get_plan_by_day(day)

            tk.Frame(self.scrollable_frame, height=1, bg="#dddddd").grid(
                row=current_row, column=0, columnspan=6, sticky="ew", pady=2
            )
            current_row += 1

            tk.Label(self.scrollable_frame, text=date_str, font=row_font, fg=row_fg, bg="#f9f9f9").grid(
                row=current_row, column=0, padx=15, sticky="nw"
            )

            lbl_day = tk.Label(self.scrollable_frame, text=day, font=row_font, 
                           fg="#2196F3" if not is_today else row_fg, bg="#f9f9f9", cursor="hand2")
            lbl_day.grid(row=current_row, column=1, padx=15, sticky="nw")

            lbl_day.bind("<Double-1>", lambda e, d=day: self.show_day_details(d))

            if not meals_for_day:
                tk.Label(self.scrollable_frame, text="-- No meals --", font=FONT_SMALL, bg="#f9f9f9", fg="grey").grid(
                    row=current_row, column=2, padx=15, sticky="w"
                )
                current_row += 1
            else:
                for meal_entry in meals_for_day:
                    db_id, name, cals, cost = meal_entry

                    tk.Label(self.scrollable_frame, text=name, font=row_font, bg="#f9f9f9", fg=row_fg).grid(
                        row=current_row, column=2, padx=15, sticky="w"
                    )
                    tk.Label(self.scrollable_frame, text=f"{cals} kcal", font=row_font, bg="#f9f9f9", fg=row_fg).grid(
                        row=current_row, column=3, padx=15, sticky="w"
                    )

                    tk.Label(self.scrollable_frame, text=f"{cost:.2f} €", font=row_font, bg="#f9f9f9", fg=row_fg).grid(
                        row=current_row, column=4, padx=15, sticky="w"
                    )

                    btn_del = tk.Button(
                        self.scrollable_frame, text="✕", fg="red", font=("Arial", 8, "bold"), 
                        command=lambda eid=db_id: self.delete_from_plan(eid), 
                        relief="flat", bg="#f9f9f9", cursor="hand2"
                    )
                    btn_del.grid(row=current_row, column=5, padx=10)

                    total_cals += cals
                    total_cost += cost
                    current_row += 1

        self.lbl_total_cals.config(text=f"Weekly Calories Total: {total_cals} kcal")
        self.lbl_total_cost.config(text=f"Weekly Cost Total: {total_cost:.2f} €")

    def show_day_details(self, day):
        meals = get_plan_by_day(day)
        prof = get_profile()
        target_cals = prof[4] 
        
        top = tk.Toplevel(self)
        top.title(f"Details for {day}")
        top.geometry("350x400")
        
        tk.Label(top, text=f"Detailed Plan: {day}", font=FONT_TITLE).pack(pady=10)
        
        total_day_cals = 0
        meal_strings = []
        for m in meals:
            meal_strings.append(f"• {m[1]} ({m[2]} kcal)")
            total_day_cals += m[2]
            
        txt_meals = tk.Text(top, font=FONT_NORMAL, height=10, bg="#f9f9f9", bd=0)
        txt_meals.pack(padx=20, pady=5)
        txt_meals.insert("1.0", "\n".join(meal_strings) if meal_strings else "No meals planned.")
        txt_meals.config(state="disabled")
        
        leftover = target_cals - total_day_cals
        color = "green" if leftover >= 0 else "red"
        
        summary = (
            f"Total Daily Calories: {total_day_cals} kcal\n"
            f"Target: {target_cals} kcal\n"
            f"Leftover: {leftover} kcal"
        )
        tk.Label(top, text=summary, font=FONT_NORMAL, fg=color).pack(pady=10)

    def delete_from_plan(self, entry_id): 
        remove_from_plan(entry_id)
        self.refresh_weekly_plan_ui()

    def add_to_weekly_plan(self, day):
        selection = self.meal_listbox.curselection()
        if not selection: return

        meal = self.current_meals[selection[0]]
        add_to_plan(day, meal[1], meal[2], meal[6])
        
        self.refresh_weekly_plan_ui()

    def remove_meal(self):
        selection = self.meal_listbox.curselection()
        if not selection: return
        
        meal = self.current_meals[selection[0]]
        meal_id = meal[0]
        meal_name = meal[1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {meal_name}?"):
            delete_meal(meal_id)
            remove_from_plan_by_name(meal_name)
            self.refresh_meal_list()
            self.refresh_weekly_plan_ui()

    def edit_meal(self):
        selection = self.meal_listbox.curselection()
        if not selection: return
        
        meal = self.current_meals[selection[0]]
        meal_id = meal[0]

        top = tk.Toplevel(self)
        top.title("Edit Meal")
        top.geometry("400x550")

        edit_entries = {}
        # Pre-fill standard entries
        for i, field in enumerate(self.fields):
            tk.Label(top, text=f"{field}:", font=FONT_NORMAL).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = tk.Entry(top, font=FONT_NORMAL)
            entry.insert(0, str(meal[i+1]) if meal[i+1] is not None else "")
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            edit_entries[field] = entry

        # Recipe Edit Area
        tk.Label(top, text="Recipe:", font=FONT_NORMAL).grid(row=6, column=0, padx=10, pady=5, sticky="ne")
        edit_recipe = tk.Text(top, font=FONT_NORMAL, width=25, height=6, wrap="word")
        edit_recipe.insert("1.0", meal[7] if meal[7] else "")
        edit_recipe.grid(row=6, column=1, padx=10, pady=5, sticky="w")


        
        def save_edits():
            try:
                old_name = meal[1] 
                
                new_name = edit_entries["Name"].get().strip()
                new_cals = int(edit_entries["Calories"].get() or 0)
                new_prot = int(edit_entries["Proteins"].get() or 0)
                new_carb = int(edit_entries["Carbs"].get() or 0)
                new_fats = int(edit_entries["Fats"].get() or 0)
                cost_in = edit_entries["Cost"].get().strip().replace(',', '.')
                new_cost = float(cost_in) if cost_in else 0.0
                new_recipe = edit_recipe.get("1.0", tk.END).strip()

                update_meal(meal_id, new_name, new_cals, new_prot, new_carb, new_fats, new_cost, new_recipe)
                
                from db.weeklyplan import update_weekly_entries_by_name
                update_weekly_entries_by_name(old_name, new_name, new_cals, new_cost)

                self.refresh_meal_list()
                self.refresh_weekly_plan_ui()
                top.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Check your numbers!", parent=top)

        tk.Button(top, text="Update", command=save_edits, bg="#2196F3", fg="white", font=FONT_NORMAL).grid(row=7, column=0, columnspan=2, pady=20)