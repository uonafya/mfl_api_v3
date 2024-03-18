--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6
-- Dumped by pg_dump version 14.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: users_mfloauthapplication; Type: TABLE DATA; Schema: public; Owner: -
--

INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (5, 'xMddOofHI0jOKboVxdoKAXWKpkEQAP0TuloGpfj5', '', 'confidential', 'password', 'PHrUzCRFm9558DGa6Fh1hEvSCh3C9Lijfq8sbCMZhZqmANYV5ZP04mUXGJdsrZLXuZG4VCmvjShdKHwU6IRmPQld5LDzvJoguEP8AAXGJhrqfLnmtFXU3x2FO1nWLxUx', 'mfl-public-frontend', false, 2512, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (6, '5O1KlpwBb96ANWe27ZQOpbWSF4DZDm4sOytwdzGv', '', 'confidential', 'password', 'PqV0dHbkjXAtJYhY9UOCgRVi5BzLhiDxGU91kbt5EoayQ5SYOoJBYRYAYlJl2RetUeDMpSvhe9DaQr0HKHan0B9ptVyoLvOqpekiOmEqUJ6HZKuIoma0pvqkkKDU9GPv', 'mfl-admin-frontend', false, 2512, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (8, 'zzAmdUPF6MLcbLdbSkdv1MkRgYD9vuG8B8Bv4lIq', '', 'confidential', 'password', 'JdxZDwF1NlLxxDyTkRIUT6az2YQ1olm4wN8y856CkpntiiRP2XqLPueDpUR3OZvPDxdiyZ4P2lNajoJLdGpS8ZmwGYNOx65qK3jXCndjbbfBZF8Uu0eDTOB4adkJQCnr', 'nivi', false, 3590, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (7, 'BoeWBMW0VP2uAkOgP4QV0iJMkhJ9lLjrWzFXMSjN', '', 'confidential', 'password', 'mRBG1zr436ymuvOmH3TQOcaumAs17Age8YQMIeOVgg7zKibnLjSFdMkSQDVC9LHKzNA44hw4JhAcN8rOWFPmsqHIpAAVaWRFPk3Ol4aEZZGpz7npuqyvnCNLOoUzE4GZ', 'ihris', false, 3590, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (9, 'GOEiK2wdDV8699iCo46ItCe8w9RdRbm3tEINuY2t', '', 'confidential', 'password', 'WFkiChHV0XTSx85yHfQRdn0jdDaoxUrRMhZKdSZtS21QkcDj4SRlfOu0oNrUo7LfeKfWimvONxTC9jV6r43srCg549DkMI6ro7DkFi9gZONKkgfYS0yngYxZ4a12w4FL', 'kemsa', false, 3590, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (10, 'jTDHUylDGzIrpmwOyzeqRrXyOyK37AwWt0q5ATVr', '', 'confidential', 'password', 'sWjAfrFCFoquim2cGDgyYXttfzXi3BeDmyFr7yeoxJC9ziNS8DQe9a1ozQDmZhDAyQlwQalUvrD0tak2cGxN2rSVGghkxiMLvDRz0g1fIwhTjWcOuNECfB1O0lFTcduN', 'Living Goods', false, 3590, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (11, 'PXdoFNdTHLNAawJsC5pXe9IJNqgse7W4NZCmbecQ', '', 'public', 'password', 'lB9bU8kTw02pgt0JpWonzcXALCcleSgSnCrusdDKFsxa0JAk1pqdCZtIKiki3zHo9BQmwVKmR4pX7d5pFDjkj9WuEF5uvy6SXR2pQF3of1PXsSasVwoHXOUjxdA6vaIj', 'healthit', true, 3590, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (12, 'qxblJCALzKXunUhNUQZpbeQLM9OTvscTYLbQ1oEY', '', 'public', 'password', 'dkwLqoQytFd4zXmPRUXsy2Q4fyRKqy7TAov5OewC2S7iWL58fwCnHyTwYBUMu7fOG091LeADDUgsqeFX446GS2GCDZ5Y6KxlvC3RgRjdSE1sXJIkCpHHfMihPMnUOnU9', 'cpims', false, 3590, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (13, 'EYh3MUTiKe8zbo96hXoJ6J6ZLOEzImvZfm9x7e2J', '', 'confidential', 'password', '34lFr4q3j14tklQgPx4Sl686ABqQi7BHGuYDKFZj6FAdjL7PcVtF0Jc6CnbokiJAH7f81CKWY812yzOT0gSMO5IO2WhU7ABAxD26yZ0DWLZ2wNLA9SVRa4FY7SiWC2Ga', 'Demo / Docs Application', false, 6, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (14, 'dGZ0s7zQPdm8TS6zxoVRGysOCLr6UwYxeNPzlNHq', '', 'confidential', 'password', '6ZnjkKs4ZgzdSM5uLkFfaSX1v97BkOI2au5zuk5RyjxEW9RgLUd0V06PwYLieXAsSjTqt6BPzeTXy2uD6SGiLyAoIR03U0mcIiafh4GBLB2SeT4Z0a11r1rpNZOfPO3e', 'Demo / Docs Application', false, 6, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (15, '6hmC9PFKCkKY1c05bsEvRzfUoqU04VWvmoBH3hfa', '', 'confidential', 'password', 'IY1qb0RiWiXsojWTe2dhbLPgFEBOLHpoBkq2FkG87OrpHy2HJniCbd9J7PT4s8BFIIDm8cozAZ6aqQ1samY74ZmJi3agb8kHcFTYK2twcqx9DJYiCDk6HplpVxHBTCjv', 'Demo / Docs Application', false, 6, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (16, 'PaHdFfq88OCkoFITVeGzTu9t4ChWwDPOne0PG9Pj', '', 'confidential', 'password', '6MALpn2iNuj0s0Ozctg3xkCXZMRbIZYTdwY80PZ3f2KPsDqTJdPGfFpY5Ls4aqYfdUcT4GPyHXFzSc824VBUU9rZ9n7ozqKfxIhjBAMtE8UNx06RdGriFnh8wjeg1IGd', 'Demo / Docs Application', false, 6, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (17, '2hZfc4BmKCy5xKk70M5kFE8Kdwt0vpArGuctsfLR', '', 'confidential', 'password', 'yMo3LaP5zU8wZ9wC1ppaylCp6pOSGJbAltk7iWzoESk0GI5fhlKAFeLTWjdNA9LHhD39OVSmQ08OFbwUIhz7Nb2hRB9uuBnWo57kGBoKoQlcm3MkeXMRi8geTG5a3YLp', 'Demo / Docs Application', false, 6, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');
INSERT INTO public.oauth2_provider_application (id, client_id, redirect_uris, client_type, authorization_grant_type, client_secret, name, skip_authorization, user_id, created, updated, algorithm, post_logout_redirect_uris) VALUES (18, 'VhqBj4nXDcjfjUvnlMd8Rl4A14pJar3xBfEJtkZq', '', 'confidential', 'password', 'Ih2ktgZ1TLUByQV2HvyvqUJ8MstFPoGafAIDCt0ga6lNCYn7Rwp8SAD5t5IIwYZ6uSLZxUybU2SbVY7HrNRz948vPW45TO0J7aYoQQH5Ql5mxdDAeqa47KE0ZP9xXhkt', 'Demo / Docs Application', false, 6, '2023-12-06 16:25:36.688299+03', '2023-12-07 17:35:33.982125+03', '', '');


--
-- Name: users_mfloauthapplication_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_mfloauthapplication_id_seq', 18, true);


--
-- PostgreSQL database dump complete
--

