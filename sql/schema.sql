-- module home's models
CREATE TABLE public.h1 (
       id SERIAL,
       val TEXT,
       PRIMARY KEY(id)
);

CREATE TABLE public.h2 (
       id SERIAL,
       val TEXT,
       val2 TEXT,
       PRIMARY KEY(id)
);

-- module mod1's models
CREATE SCHEMA mod1;
CREATE TABLE mod1.h1 (
       id SERIAL,
       val2 TEXT,
       PRIMARY KEY(id)
);

-- module mod3's models
CREATE TABLE public.page (
       id SERIAL,
       url TEXT,
       PRIMARY KEY(id)
);
CREATE UNIQUE INDEX page_url_udx ON public.page(LOWER(url));

CREATE TABLE public.tag (
       id SERIAL,
       name TEXT,
       PRIMARY KEY(id)
);
CREATE UNIQUE INDEX tag_name_udx ON public.tag(LOWER(name));

CREATE TABLE public.page_tags (
       page_id INT NOT NULL,
       tag_id INT NOT NULL,
       PRIMARY KEY(page_id, tag_id),
       FOREIGN KEY(page_id) REFERENCES public.page(id),
       FOREIGN KEY(tag_id) REFERENCES public.tag(id)
);
CREATE UNIQUE INDEX page_tags_tag_page_id_udx ON public.page_tags (tag_id, page_id);
