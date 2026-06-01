import os
import threading
import traceback
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

import pandas as pd

try:
    import matlab.engine
except Exception:
    matlab = None


class PETROIToolbox:
    def __init__(self, root: tk.Tk):
        self.root = root
        logo_path = os.path.join(os.path.dirname(__file__), "logo.png")

        img = Image.open(logo_path)
        img = img.resize((48, 48))   # adjust size if needed
        self.logo_img = ImageTk.PhotoImage(img)
        self.root.title("PET ROI Extraction Toolbox (SPM12)")
        self.root.geometry("1100x760")
        self.root.minsize(1000, 760)
        self.root.configure(bg="#eef4fb")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.pet_files = []

        self.atlas_var = tk.StringVar()
        self.mask_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.roi_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Ready")

        self._running = False
        self.progress = None
        self.status_label = None
        self.run_btn = None
        self.preview_text = None
        self.pet_count_label = None

        self._setup_styles()
        self._build_ui()

    def _setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        BG = "#eef4fb"
        CARD = "#ffffff"
        BORDER = "#d6e2f0"
        PRIMARY = "#2f6fed"
        PRIMARY_HOVER = "#2459bf"
        SECONDARY = "#e8f0fe"
        TEXT = "#1f2937"
        MUTED = "#5f6b7a"

        style.configure("Main.TFrame", background=BG)

        style.configure(
            "Card.TLabelframe",
            background=CARD,
            bordercolor=BORDER,
            borderwidth=1,
            relief="solid",
            padding=10,
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=CARD,
            foreground=TEXT,
            font=("Segoe UI", 11, "bold"),
        )

        style.configure(
            "Header.TLabel",
            background=BG,
            foreground=PRIMARY,
            font=("Segoe UI", 23, "bold"),
        )

        style.configure(
            "SubHeader.TLabel",
            background=BG,
            foreground=MUTED,
            font=("Segoe UI", 10),
        )

        style.configure(
            "Info.TLabel",
            background=CARD,
            foreground=PRIMARY,
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "Field.TLabel",
            background=CARD,
            foreground=TEXT,
            font=("Segoe UI", 10),
        )

        style.configure(
            "Primary.TButton",
            background=PRIMARY,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=(14, 10),
            borderwidth=0,
            focusthickness=0,
        )
        style.map(
            "Primary.TButton",
            background=[("active", PRIMARY_HOVER), ("pressed", PRIMARY_HOVER)],
        )

        style.configure(
            "Secondary.TButton",
            background=SECONDARY,
            foreground=PRIMARY,
            font=("Segoe UI", 10),
            padding=(12, 9),
            borderwidth=0,
            focusthickness=0,
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#dbeafe"), ("pressed", "#dbeafe")],
        )

        style.configure(
            "TEntry",
            padding=6,
            fieldbackground="#ffffff",
            foreground=TEXT,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
        )

        style.configure(
            "Blue.Horizontal.TProgressbar",
            troughcolor="#dbeafe",
            background=PRIMARY,
            thickness=12,
            bordercolor="#dbeafe",
            lightcolor=PRIMARY,
            darkcolor=PRIMARY,
        )

    def _build_ui(self):
        container = ttk.Frame(self.root, style="Main.TFrame")
        container.pack(fill="both", expand=True, padx=18, pady=18)

        container.columnconfigure(0, weight=3)
        container.columnconfigure(1, weight=2)
        container.rowconfigure(1, weight=1)

        top = ttk.Frame(container, style="Main.TFrame")
        top.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 14))

        left = ttk.Frame(container, style="Main.TFrame")
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 12))

        right = ttk.Frame(container, style="Main.TFrame")
        right.grid(row=1, column=1, sticky="nsew")

        title_frame = ttk.Frame(top, style="Main.TFrame")
        title_frame.pack(anchor="w", padx=8, pady=(6, 2))

        logo_label = ttk.Label(
            title_frame,
            image=self.logo_img,
            background="#eef4fb"
            )
        logo_label.pack(side="left", padx=(0, 10))

        title = ttk.Label(
            title_frame,
            text="PET ROI Extraction Toolbox",
            style="Header.TLabel",
            )
        title.pack(side="left")

        subtitle = ttk.Label(
            top,
            text=(
                "Python GUI with MATLAB/SPM12 backend for atlas-based ROI extraction "
                "from preprocessed PET SUV images in MNI space."
            ),
            style="SubHeader.TLabel",
            wraplength=1000,
            justify="left",
        )
        subtitle.pack(anchor="w", padx=8, pady=(0, 8))

        # LEFT SIDE
        pet_frame = ttk.LabelFrame(left, text="PET Images", style="Card.TLabelframe")
        pet_frame.pack(fill="x", pady=(0, 12))

        btn_row = ttk.Frame(pet_frame, style="Main.TFrame")
        btn_row.pack(fill="x", padx=8, pady=8)

        ttk.Button(
            btn_row,
            text="Load PET Images",
            command=self._pick_pet_files,
            style="Primary.TButton",
        ).pack(side="left")

        ttk.Button(
            btn_row,
            text="Clear PET List",
            command=self._clear_pet_files,
            style="Secondary.TButton",
        ).pack(side="left", padx=8)

        self.pet_count_label = ttk.Label(
            pet_frame,
            text="No PET images selected",
            style="Field.TLabel",
        )
        self.pet_count_label.pack(anchor="w", padx=8, pady=(0, 6))

        pet_list_frame = ttk.Frame(pet_frame, style="Main.TFrame")
        pet_list_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

        self.pet_listbox = tk.Listbox(
            pet_list_frame,
            height=7,
            font=("Segoe UI", 10),
            bg="#ffffff",
            fg="#1f2937",
            relief="solid",
            borderwidth=1,
        )
        self.pet_listbox.pack(side="left", fill="both", expand=True)

        pet_scroll = ttk.Scrollbar(pet_list_frame, orient="vertical", command=self.pet_listbox.yview)
        pet_scroll.pack(side="right", fill="y")
        self.pet_listbox.configure(yscrollcommand=pet_scroll.set)

        atlas_frame = ttk.LabelFrame(left, text="Atlas / Mask / Output", style="Card.TLabelframe")
        atlas_frame.pack(fill="x", pady=(0, 12))

        self._file_row(atlas_frame, 0, "Atlas (MNI .nii/.img)", self.atlas_var, self._pick_atlas)
        self._file_row(atlas_frame, 1, "GM mask (optional)", self.mask_var, self._pick_mask)
        self._file_row(atlas_frame, 2, "Output CSV", self.output_var, self._pick_output_csv)

        roi_frame = ttk.LabelFrame(left, text="ROI Selection", style="Card.TLabelframe")
        roi_frame.pack(fill="x", pady=(0, 12))

        ttk.Label(
            roi_frame,
            text="Enter ROI numbers separated by commas, or leave blank to auto-detect from the atlas.",
            style="Field.TLabel",
        ).pack(anchor="w", padx=8, pady=(8, 4))

        ttk.Entry(roi_frame, textvariable=self.roi_var).pack(fill="x", padx=8, pady=(0, 8))

        help_frame = ttk.LabelFrame(left, text="Notes", style="Card.TLabelframe")
        help_frame.pack(fill="x")

        notes = (
            "• PET images should already be normalized to MNI space.\n"
            "• Atlas must also be in MNI space.\n"
            "• ROI label 0 is ignored automatically.\n"
            "• If a GM mask is provided, PET values are masked before ROI extraction.\n"
            "• Output table will contain one row per subject and one column per ROI."
        )

        ttk.Label(
            help_frame,
            text=notes,
            style="Field.TLabel",
            justify="left",
        ).pack(anchor="w", padx=8, pady=8)

        # RIGHT SIDE
        actions = ttk.LabelFrame(right, text="Actions", style="Card.TLabelframe")
        actions.pack(fill="x", pady=(0, 12))

        self.run_btn = ttk.Button(
            actions,
            text="Run ROI Extraction",
            command=self.run_extraction,
            style="Primary.TButton",
        )
        self.run_btn.pack(fill="x", pady=(4, 8))

        ttk.Button(
            actions,
            text="Open Output Folder",
            command=self.open_output_folder,
            style="Secondary.TButton",
        ).pack(fill="x", pady=4)

        status_frame = ttk.LabelFrame(right, text="Status", style="Card.TLabelframe")
        status_frame.pack(fill="x", pady=(0, 12))

        self.status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            style="Info.TLabel",
        )
        self.status_label.pack(anchor="w", padx=8, pady=(6, 6))

        self.progress = ttk.Progressbar(
            status_frame,
            mode="indeterminate",
            style="Blue.Horizontal.TProgressbar",
        )
        self.progress.pack(fill="x", padx=8, pady=(0, 8))

        preview_frame = ttk.LabelFrame(right, text="Results Preview", style="Card.TLabelframe")
        preview_frame.pack(fill="both", expand=True)

        self.preview_text = tk.Text(
            preview_frame,
            wrap="none",
            bg="#0f172a",
            fg="#e5e7eb",
            insertbackground="white",
            relief="flat",
            borderwidth=0,
            font=("Consolas", 10),
            padx=10,
            pady=10,
        )
        self.preview_text.pack(side="left", fill="both", expand=True)

        y_scroll = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        y_scroll.pack(side="right", fill="y")
        self.preview_text.configure(yscrollcommand=y_scroll.set)

        self.preview_text.tag_configure("error", foreground="#fca5a5")
        self.preview_text.tag_configure("success", foreground="#86efac")
        self.preview_text.tag_configure("info", foreground="#93c5fd")

        self._append_preview("Load PET images, atlas, and output CSV, then click 'Run ROI Extraction'.")

    def _file_row(self, parent, row, label, variable, command):
        ttk.Label(parent, text=label, style="Field.TLabel").grid(
            row=row, column=0, sticky="w", padx=8, pady=8
        )
        ttk.Entry(parent, textvariable=variable).grid(
            row=row, column=1, sticky="ew", padx=8, pady=8
        )
        ttk.Button(
            parent,
            text="Browse",
            command=command,
            style="Secondary.TButton",
        ).grid(row=row, column=2, padx=8, pady=8)
        parent.columnconfigure(1, weight=1)

    def _append_preview(self, text: str):
        lower = text.lower()
        tag = None
        if text.startswith("ERROR") or "failed" in lower:
            tag = "error"
        elif "completed" in lower or "success" in lower:
            tag = "success"
        elif "loading" in lower or "running" in lower or "launching" in lower:
            tag = "info"

        self.preview_text.insert("end", text.rstrip() + "\n", tag)
        self.preview_text.see("end")
        self.root.update_idletasks()

    def _set_status_color(self, color):
        if self.status_label is not None:
            self.status_label.configure(foreground=color)

    def _set_run_state(self, state: str):
        if self.run_btn is not None:
            self.run_btn.configure(state=state)

    def _pick_pet_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[("NIfTI/Analyze", "*.nii *.img")]
        )
        if files:
            self.pet_files = list(files)
            self._refresh_pet_list()

    def _clear_pet_files(self):
        self.pet_files = []
        self._refresh_pet_list()

    def _refresh_pet_list(self):
        self.pet_listbox.delete(0, "end")
        for f in self.pet_files:
            self.pet_listbox.insert("end", os.path.basename(f))

        if self.pet_files:
            self.pet_count_label.config(text=f"{len(self.pet_files)} PET image(s) selected")
        else:
            self.pet_count_label.config(text="No PET images selected")

    def _pick_atlas(self):
        path = filedialog.askopenfilename(filetypes=[("NIfTI/Analyze", "*.nii *.img")])
        if path:
            self.atlas_var.set(path)

    def _pick_mask(self):
        path = filedialog.askopenfilename(filetypes=[("NIfTI/Analyze", "*.nii *.img")])
        if path:
            self.mask_var.set(path)

    def _pick_output_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
        )
        if path:
            self.output_var.set(path)

    def open_output_folder(self):
        out_csv = self.output_var.get().strip()
        if out_csv:
            folder = os.path.dirname(out_csv)
            if folder and os.path.isdir(folder):
                os.startfile(folder)
                return
        messagebox.showinfo("Output folder", "Set a valid output CSV path first.")

    def _validate(self):
        errors = []

        if not self.pet_files:
            errors.append("Please load at least one PET image.")

        atlas = self.atlas_var.get().strip()
        if not atlas:
            errors.append("Atlas file is required.")
        elif not os.path.isfile(atlas):
            errors.append(f"Atlas file does not exist: {atlas}")

        mask = self.mask_var.get().strip()
        if mask and not os.path.isfile(mask):
            errors.append(f"GM mask does not exist: {mask}")

        out_csv = self.output_var.get().strip()
        if not out_csv:
            errors.append("Output CSV path is required.")

        roi_txt = self.roi_var.get().strip()
        if roi_txt:
            try:
                _ = [float(x.strip()) for x in roi_txt.split(",") if x.strip()]
            except ValueError:
                errors.append("ROI list must contain numbers separated by commas.")

        if errors:
            messagebox.showerror("Missing/invalid input", "\n".join(errors))
            return False

        return True

    def _parse_roi_list(self):
        roi_txt = self.roi_var.get().strip()
        if not roi_txt:
            return []
        return [float(x.strip()) for x in roi_txt.split(",") if x.strip()]

    def run_extraction(self):
        if self._running:
            return
        if not self._validate():
            return

        self._running = True
        self._set_run_state("disabled")
        self.status_var.set("Running ROI extraction...")
        self._set_status_color("#2f6fed")

        if self.progress is not None:
            self.progress.start(10)

        self._append_preview("Running ROI extraction...")
        threading.Thread(target=self._run_worker, daemon=True).start()

    def _run_worker(self):
        try:
            if matlab is None:
                raise RuntimeError("MATLAB Engine for Python is not installed in this environment.")

            self._append_preview("Launching MATLAB engine...")
            eng = matlab.engine.start_matlab()

            app_dir = Path(__file__).resolve().parent
            eng.addpath(str(app_dir), nargout=0)

            pet_files_ml = self.pet_files

            roi_list = self._parse_roi_list()
            roi_ml = matlab.double([roi_list]) if roi_list else matlab.double([])

            mask_path = self.mask_var.get().strip()
            atlas_path = self.atlas_var.get().strip()
            out_csv = self.output_var.get().strip()

            self._append_preview("Calling MATLAB SPM ROI extraction...")
            result_csv = eng.pet_roi_extract(
                pet_files_ml,
                atlas_path,
                mask_path,
                roi_ml,
                out_csv,
                nargout=1,
            )

            self._append_preview(f"Completed successfully. Output: {result_csv}")

            df = pd.read_csv(result_csv)
            self.preview_text.delete("1.0", "end")
            self.preview_text.insert("end", df.to_string(index=False))

            self.status_var.set("ROI extraction completed successfully")
            self._set_status_color("#15803d")

            messagebox.showinfo(
                "Done",
                f"ROI extraction completed successfully.\n\nOutput file:\n{result_csv}",
            )

        except Exception as e:
            tb = traceback.format_exc()
            self._append_preview(f"ERROR: {e}")
            self._append_preview(tb)

            self.status_var.set("ROI extraction failed")
            self._set_status_color("#b91c1c")

            messagebox.showerror("ROI extraction failed", f"{e}\n\nSee preview/log for details.")

        finally:
            if self.progress is not None:
                self.progress.stop()

            self._running = False
            self._set_run_state("normal")


def main():
    root = tk.Tk()
    app = PETROIToolbox(root)
    root.mainloop()


if __name__ == "__main__":
    main()
