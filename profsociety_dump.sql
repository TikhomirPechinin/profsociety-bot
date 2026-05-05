--
-- PostgreSQL database dump
--

\restrict eaN2u6LbHnMFinKaZr0cruHsO6XY67RqBjZY2rFY29NrQKBgdMPVdhCo2rxUVHk

-- Dumped from database version 14.22 (Ubuntu 14.22-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.22 (Ubuntu 14.22-0ubuntu0.22.04.1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: additional_scholarship; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.additional_scholarship (
    id integer NOT NULL,
    name text,
    amount numeric,
    is_fixed boolean DEFAULT true
);


ALTER TABLE public.additional_scholarship OWNER TO postgres;

--
-- Name: additional_scholarship_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.additional_scholarship_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.additional_scholarship_id_seq OWNER TO postgres;

--
-- Name: additional_scholarship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.additional_scholarship_id_seq OWNED BY public.additional_scholarship.id;


--
-- Name: events; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.events (
    id integer NOT NULL,
    event_date date NOT NULL,
    title text NOT NULL,
    location text,
    description text
);


ALTER TABLE public.events OWNER TO postgres;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO postgres;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: members; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.members (
    vk_id bigint,
    full_name text NOT NULL,
    group_name text,
    joined_at date DEFAULT CURRENT_DATE,
    is_member boolean DEFAULT true,
    id integer NOT NULL
);


ALTER TABLE public.members OWNER TO postgres;

--
-- Name: members_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.members_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.members_id_seq OWNER TO postgres;

--
-- Name: members_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.members_id_seq OWNED BY public.members.id;


--
-- Name: scholarship_settings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scholarship_settings (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    value numeric NOT NULL
);


ALTER TABLE public.scholarship_settings OWNER TO postgres;

--
-- Name: scholarship_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.scholarship_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.scholarship_settings_id_seq OWNER TO postgres;

--
-- Name: scholarship_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.scholarship_settings_id_seq OWNED BY public.scholarship_settings.id;


--
-- Name: social_scholarship; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.social_scholarship (
    id integer NOT NULL,
    category text,
    amount numeric,
    description text
);


ALTER TABLE public.social_scholarship OWNER TO postgres;

--
-- Name: social_scholarship_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.social_scholarship_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.social_scholarship_id_seq OWNER TO postgres;

--
-- Name: social_scholarship_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.social_scholarship_id_seq OWNED BY public.social_scholarship.id;


--
-- Name: user_sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_sessions (
    vk_id bigint NOT NULL,
    current_scenario text,
    context_data text,
    last_activity timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_sessions OWNER TO postgres;

--
-- Name: additional_scholarship id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.additional_scholarship ALTER COLUMN id SET DEFAULT nextval('public.additional_scholarship_id_seq'::regclass);


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Name: members id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members ALTER COLUMN id SET DEFAULT nextval('public.members_id_seq'::regclass);


--
-- Name: scholarship_settings id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scholarship_settings ALTER COLUMN id SET DEFAULT nextval('public.scholarship_settings_id_seq'::regclass);


--
-- Name: social_scholarship id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.social_scholarship ALTER COLUMN id SET DEFAULT nextval('public.social_scholarship_id_seq'::regclass);


--
-- Data for Name: additional_scholarship; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.additional_scholarship (id, name, amount, is_fixed) FROM stdin;
1	ПГАС (Повышенная гос. академическая)	15800	t
3	Стипендия Правительства РФ	5000	t
4	Стипендия Президента РФ	7000	t
2	Именная стипендия	1350	f
5	Повышение к ГАС (за отличные оценки)	2000	t
6	Повышенная социальная стипендия	7300	t
\.


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.events (id, event_date, title, location, description) FROM stdin;
1	2026-04-23	Кейс: Организация восстановления разрушенной инфраструктуры	хгу	удет весело
\.


--
-- Data for Name: members; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.members (vk_id, full_name, group_name, joined_at, is_member, id) FROM stdin;
56567567	Печинин Тихомир Олегович	565656	2026-04-13	t	3
165645	Тестовый Студент	ИТ-222	2026-04-13	t	1
\N	Печинин Тихомир Олегович	222	2026-04-14	t	7
\N	Иванов Иван Иванович	Д-322	2026-04-14	t	8
\.


--
-- Data for Name: scholarship_settings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scholarship_settings (id, name, value) FROM stdin;
1	ГАС (ВО)	4700
2	Повышение к ГАС (ВО)	1175
3	Социальная (ВО)	5200
4	Повышенная социальная (ВО)	20100
5	ПГАС (ВО)	18000
6	ГАС (СПО федеральный)	1600
7	Повышение к ГАС (СПО федеральный)	400
8	Социальная (СПО федеральный)	2320
9	ГАС (СПО региональный)	1545
10	Повышение к ГАС (СПО региональный)	0
11	Социальная (СПО региональный)	2317
\.


--
-- Data for Name: social_scholarship; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.social_scholarship (id, category, amount, description) FROM stdin;
1	Сирота	5400	Дети-сироты и оставшиеся без попечения родителей
2	Инвалид I/II группы	5400	Студенты-инвалиды I и II группы
3	Чернобылец	5400	Пострадавшие от аварии на ЧАЭС
4	Малообеспеченные	3000	Студенты из малообеспеченных семей
\.


--
-- Data for Name: user_sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_sessions (vk_id, current_scenario, context_data, last_activity) FROM stdin;
\.


--
-- Name: additional_scholarship_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.additional_scholarship_id_seq', 6, true);


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.events_id_seq', 1, true);


--
-- Name: members_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.members_id_seq', 8, true);


--
-- Name: scholarship_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.scholarship_settings_id_seq', 11, true);


--
-- Name: social_scholarship_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.social_scholarship_id_seq', 4, true);


--
-- Name: additional_scholarship additional_scholarship_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.additional_scholarship
    ADD CONSTRAINT additional_scholarship_pkey PRIMARY KEY (id);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- Name: members members_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.members
    ADD CONSTRAINT members_pkey PRIMARY KEY (id);


--
-- Name: scholarship_settings scholarship_settings_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scholarship_settings
    ADD CONSTRAINT scholarship_settings_name_key UNIQUE (name);


--
-- Name: scholarship_settings scholarship_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scholarship_settings
    ADD CONSTRAINT scholarship_settings_pkey PRIMARY KEY (id);


--
-- Name: social_scholarship social_scholarship_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.social_scholarship
    ADD CONSTRAINT social_scholarship_pkey PRIMARY KEY (id);


--
-- Name: user_sessions user_sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_sessions
    ADD CONSTRAINT user_sessions_pkey PRIMARY KEY (vk_id);


--
-- PostgreSQL database dump complete
--

\unrestrict eaN2u6LbHnMFinKaZr0cruHsO6XY67RqBjZY2rFY29NrQKBgdMPVdhCo2rxUVHk

