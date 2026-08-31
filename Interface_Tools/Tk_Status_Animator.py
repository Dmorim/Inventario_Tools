class TextAnimator:
    """Agenda uma atualização periódica de texto em um widget Tkinter.

    Centraliza a lógica de `after()` para evitar duplicação de timers e
    falhas ao tentar atualizar widgets já destruídos.
    """

    def __init__(self, widget, interval_ms: int = 500):
        self.widget = widget
        self.interval_ms = interval_ms
        self._job_id = None
        self._tick_fn = None

    def start(self, tick_fn):
        self.cancel()
        self._tick_fn = tick_fn
        self._run_tick()

    def _run_tick(self):
        if self.widget is None or not self.widget.winfo_exists():
            self._job_id = None
            return

        try:
            if self._tick_fn is not None:
                self._tick_fn()
            self._job_id = self.widget.after(self.interval_ms, self._run_tick)
        except Exception:
            self._job_id = None

    def cancel(self):
        if self._job_id is None:
            return

        try:
            if self.widget is not None and self.widget.winfo_exists():
                self.widget.after_cancel(self._job_id)
        except Exception:
            pass
        finally:
            self._job_id = None

    def stop(self, final_text: str = ""):
        self.cancel()
        if self.widget is None or not self.widget.winfo_exists():
            return

        try:
            self.widget.configure(text=final_text)
        except Exception:
            pass
