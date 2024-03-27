import calendar
import tkinter as Tkinter
import tkinter.font as tkFont
from tkinter import ttk

class Calendar(ttk.Frame):
    def __init__(self, parent, firstweekday=calendar.MONDAY, **kw):
        ttk.Frame.__init__(self, parent, **kw)
        self._cal = calendar.TextCalendar(firstweekday)
        self._items = []
        self._date = None
        self._selection = None
        self.__setup_styles()
        self.__place_widgets()
        self.__config_calendar()
        self.__setup_selection('#ecffc4', '#05640e')
        self.__minsize(None)
        self._build_calendar()

    def __setup_styles(self):
        style = ttk.Style(self.master)
        arrow_layout = lambda dir: [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        proceedB = ttk.Button(self, text='Proceed', command=self.proceed_fun)
        proceedB.pack(padx=10, pady=3)
        hframe = ttk.Frame(self)
        lbtn = ttk.Button(hframe, style='L.TButton', command=self._prev_month)
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._next_month)
        self._header = ttk.Label(hframe, width=15, anchor='center')
        self._calendar = ttk.Treeview(self, show='', selectmode='none', height=7)
        hframe.pack(in_=self, side='top', pady=4, anchor='center')
        lbtn.grid(in_=hframe)
        self._header.grid(in_=hframe, column=1, row=0, padx=12)
        rbtn.grid(in_=hframe, column=2, row=0)
        self._calendar.pack(in_=self, expand=True, fill='both', side='bottom')
        for _ in range(6):
            self._items.append(self._calendar.insert('', 'end', values=''))

    def __config_calendar(self):
        cols = self._cal.formatweekheader(3).split()
        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tags='header')
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(col, width=maxwidth, minwidth=maxwidth, anchor='e')

    def __setup_selection(self, sel_bg, sel_fg):
        self._font = tkFont.Font()
        self._canvas = canvas = Tkinter.Canvas(self._calendar, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')
        canvas.place(relwidth=1.0, relheight=1.0)
        self._calendar.bind('<ButtonPress-1>', self._pressed)

    def __minsize(self, evt):
        (width, height) = self.master.geometry().split('x')
        height = height[:height.index('+')]
        self.master.minsize(width, height)

    def _build_calendar(self):
        year = self._date.year
        month = self._date.month
        header = self._cal.formatmonthname(year, month, 0)
        self._header['text'] = header.title()
        cal = self._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = ['%02d' % day if day != 0 else '' for day in week]
            self._calendar.item(item, values=fmt_week)

    def _show_selection(self, text, bbox):
        (x, y, width, height) = bbox
        textw = self._font.measure(text)
        canvas = self._canvas
        canvas.coords(canvas.text, width - textw, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)

    def _pressed(self, evt):
        x = evt.x
        y = evt.y
        widget = evt.widget
        item = widget.identify_row(y)
        column = widget.identify_column(x)
        if not column or item not in self._items:
            return None
        item_values = self._calendar.item(item)['values']
        if not item_values:
            return None
        text = item_values[int(column[1]) - 1]
        if not text:
            return None
        bbox = self._calendar.bbox(item, column)
        if not bbox:
            return None
        text = '%02d' % text
        self._selection = (text, item, column)
        self._show_selection(text, bbox)

    def _prev_month(self):
        self._selection = None
        self._canvas.place_forget()
        self._date -= calendar.timedelta(days=1)
        self._date = self._date.replace(day=1)
        self._build_calendar()

    def _next_month(self):
        self._selection = None
        self._canvas.place_forget()
        year, month = self._date.year, self._date.month
        days_in_month = calendar.monthrange(year, month)[1]
        self._date += calendar.timedelta(days=days_in_month + 1)
        self._date = self._date.replace(day=1)
        self._build_calendar()

    def proceed_fun(self):
        if self._selection:
            year = self._date.year
            month = self._date.month
            date = [int(self._selection[0]), month, year]
            print(f"{date[0]}-{date[1]}-{date[2]}")  # Just for testing, change it as per your requirement.

def test():
    root = Tkinter.Tk()
    root.title('Ttk Calendar')
    ttkcal = Calendar(root, firstweekday=calendar.SUNDAY)
    ttkcal.pack(expand=True, fill='both')
    root.mainloop()

if __name__ == '__main__':
    test()
