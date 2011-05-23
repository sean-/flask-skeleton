INSERT INTO public.h1 (val) VALUES ('h1-id1');
INSERT INTO mod1.h2 (val2) VALUES ('h2-id1'), ('h2-id2');
INSERT INTO public.h3 (val, val2) VALUES ('h3-val-1','h3-val2-1'), ('h3-val-2','h3-val2-2'), ('h3-val-3','h3-val2-3');
INSERT INTO public.page(url) VALUES ('http://127.0.0.1:5000/foo'), ('http://127.0.0.1:5000/bar');
INSERT INTO public.tag(name) VALUES ('foo_tag'),('bar_tag'),('both_tag');
INSERT INTO public.page_tags(page_id, tag_id) VALUES (1,1), (1,3), (2,2), (2,3);
