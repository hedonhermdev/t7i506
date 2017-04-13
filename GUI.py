"""T."""
import scraper
import tkinter as tk


class App(tk.Tk):
    """Tkinter app class."""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, ScrapeProfile, ScrapePost):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        intro_label = tk.Label(
            self, text="Welcome to the Instagram Scraper v2.0.")
        intro_label.grid(row=0, column=0, pady=5, padx=5)
        profile_button = tk.Button(self, text="Scrape a profile page.",
                                   command=lambda: controller.show_frame("ScrapeProfile"))
        profile_button.grid(row=1, column=1, pady=20, padx=10)
        post_button = tk.Button(self, text="Scrape a post page.",
                                command=lambda: controller.show_frame("ScrapePost"))
        post_button.grid(row=1, column=0)


class ScrapeProfile(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller


class ScrapePost(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        intro_label = tk.Label(self, text="Enter the code of the post in the input box below.\
For multiple posts, enter the posts seperated by a comma(,).")
        intro_label.grid(row=0, column=0, padx=5, pady=10)
        #POST IDs
        self.post_ids = tk.StringVar()
        input_box = tk.Entry(self, textvariable=self.post_ids)
        input_box.grid(row=1, column=0, pady=15)
        get_button = tk.Button(self, text='GO', command=self.scrape_posts)
        get_button.grid(row=2)
    def scrape_posts(self):
        posts_arr = [post_id.strip() for post_id in self.post_ids.get().split(',')]
        for post in posts_arr:
            post = scraper.PostPage(post)
            post.save_media()
            post.writetofile()
if __name__ == "__main__":
    APP = App()
    APP.mainloop()
