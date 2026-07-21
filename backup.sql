--
-- PostgreSQL database dump
--

\restrict IKEcM39LgMmhSvt6a8yEhKSpzB32M4aRgwmfdMAkradeE6PmxahdJt6ZA84zKR6

-- Dumped from database version 17.10 (Debian 17.10-1.pgdg13+1)
-- Dumped by pg_dump version 17.10 (Debian 17.10-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: alarmeventtype; Type: TYPE; Schema: public; Owner: alarm
--

CREATE TYPE public.alarmeventtype AS ENUM (
    'ARM',
    'DISARM',
    'ACTIVATE',
    'DEACTIVATE',
    'MOTION',
    'TEMPERATURE',
    'HUMIDITY',
    'CAMERA',
    'SYSTEM'
);


ALTER TYPE public.alarmeventtype OWNER TO alarm;

--
-- Name: connectiontype; Type: TYPE; Schema: public; Owner: alarm
--

CREATE TYPE public.connectiontype AS ENUM (
    'GPIO',
    'I2C',
    'SPI',
    'USB',
    'ETHERNET',
    'WIFI',
    'CSI'
);


ALTER TYPE public.connectiontype OWNER TO alarm;

--
-- Name: devicetype; Type: TYPE; Schema: public; Owner: alarm
--

CREATE TYPE public.devicetype AS ENUM (
    'SENSOR',
    'MOTOR',
    'RGB_LED',
    'BUZZER',
    'LED',
    'LCD',
    'CAMERA'
);


ALTER TYPE public.devicetype OWNER TO alarm;

--
-- Name: notificationtype; Type: TYPE; Schema: public; Owner: alarm
--

CREATE TYPE public.notificationtype AS ENUM (
    'INFO',
    'WARNING',
    'ERROR',
    'ALERT'
);


ALTER TYPE public.notificationtype OWNER TO alarm;

--
-- Name: sensortype; Type: TYPE; Schema: public; Owner: alarm
--

CREATE TYPE public.sensortype AS ENUM (
    'LDR',
    'DHT11',
    'PIR',
    'TEMPERATURE',
    'HUMIDITY'
);


ALTER TYPE public.sensortype OWNER TO alarm;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: alarm
--

CREATE TYPE public.userrole AS ENUM (
    'ADMIN',
    'USER',
    'SERVICE'
);


ALTER TYPE public.userrole OWNER TO alarm;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alarm_events; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.alarm_events (
    id integer NOT NULL,
    event_type public.alarmeventtype NOT NULL,
    user_id integer,
    device_id integer,
    location character varying(100),
    message character varying(100),
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.alarm_events OWNER TO alarm;

--
-- Name: alarm_events_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.alarm_events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.alarm_events_id_seq OWNER TO alarm;

--
-- Name: alarm_events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.alarm_events_id_seq OWNED BY public.alarm_events.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO alarm;

--
-- Name: car_plates; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.car_plates (
    id integer NOT NULL,
    plate_number character varying(7) NOT NULL,
    owner_name character varying(50),
    auto_open boolean NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.car_plates OWNER TO alarm;

--
-- Name: car_plates_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.car_plates_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.car_plates_id_seq OWNER TO alarm;

--
-- Name: car_plates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.car_plates_id_seq OWNED BY public.car_plates.id;


--
-- Name: devices; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.devices (
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    connection_type public.connectiontype NOT NULL,
    connection_identifier character varying(50) NOT NULL,
    type public.devicetype NOT NULL,
    location character varying(256),
    enabled boolean NOT NULL
);


ALTER TABLE public.devices OWNER TO alarm;

--
-- Name: devices_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.devices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.devices_id_seq OWNER TO alarm;

--
-- Name: devices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.devices_id_seq OWNED BY public.devices.id;


--
-- Name: notifications; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    title character varying(100) NOT NULL,
    message text NOT NULL,
    user_id integer,
    is_read boolean NOT NULL,
    notification_type public.notificationtype NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.notifications OWNER TO alarm;

--
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO alarm;

--
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- Name: sensor_readings; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.sensor_readings (
    id integer NOT NULL,
    sensor_id integer NOT NULL,
    value double precision NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


ALTER TABLE public.sensor_readings OWNER TO alarm;

--
-- Name: sensor_readings_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.sensor_readings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sensor_readings_id_seq OWNER TO alarm;

--
-- Name: sensor_readings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.sensor_readings_id_seq OWNED BY public.sensor_readings.id;


--
-- Name: sensors; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.sensors (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    type public.sensortype NOT NULL,
    gpio_pin integer NOT NULL,
    enabled boolean NOT NULL,
    location character varying(100)
);


ALTER TABLE public.sensors OWNER TO alarm;

--
-- Name: sensors_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.sensors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sensors_id_seq OWNER TO alarm;

--
-- Name: sensors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.sensors_id_seq OWNED BY public.sensors.id;


--
-- Name: settings; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.settings (
    id integer NOT NULL,
    key character varying(100) NOT NULL,
    value text NOT NULL,
    description text,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.settings OWNER TO alarm;

--
-- Name: settings_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.settings_id_seq OWNER TO alarm;

--
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.settings_id_seq OWNED BY public.settings.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: alarm
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash character varying(255) NOT NULL,
    role public.userrole NOT NULL,
    is_active boolean NOT NULL,
    creation_date timestamp without time zone,
    pin_hash character varying(255) NOT NULL
);


ALTER TABLE public.users OWNER TO alarm;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: alarm
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO alarm;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: alarm
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: alarm_events id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.alarm_events ALTER COLUMN id SET DEFAULT nextval('public.alarm_events_id_seq'::regclass);


--
-- Name: car_plates id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.car_plates ALTER COLUMN id SET DEFAULT nextval('public.car_plates_id_seq'::regclass);


--
-- Name: devices id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.devices ALTER COLUMN id SET DEFAULT nextval('public.devices_id_seq'::regclass);


--
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- Name: sensor_readings id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.sensor_readings ALTER COLUMN id SET DEFAULT nextval('public.sensor_readings_id_seq'::regclass);


--
-- Name: sensors id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.sensors ALTER COLUMN id SET DEFAULT nextval('public.sensors_id_seq'::regclass);


--
-- Name: settings id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.settings ALTER COLUMN id SET DEFAULT nextval('public.settings_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alarm_events; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.alarm_events (id, event_type, user_id, device_id, location, message, "timestamp") FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.alembic_version (version_num) FROM stdin;
6bfd69c86a7c
\.


--
-- Data for Name: car_plates; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.car_plates (id, plate_number, owner_name, auto_open, created_at) FROM stdin;
\.


--
-- Data for Name: devices; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.devices (id, name, connection_type, connection_identifier, type, location, enabled) FROM stdin;
\.


--
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.notifications (id, title, message, user_id, is_read, notification_type, "timestamp") FROM stdin;
\.


--
-- Data for Name: sensor_readings; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.sensor_readings (id, sensor_id, value, "timestamp") FROM stdin;
\.


--
-- Data for Name: sensors; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.sensors (id, name, type, gpio_pin, enabled, location) FROM stdin;
\.


--
-- Data for Name: settings; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.settings (id, key, value, description, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: alarm
--

COPY public.users (id, username, password_hash, role, is_active, creation_date, pin_hash) FROM stdin;
2	admin	$2b$12$RbaEggONlkAzuB2Rn/KHLe7lV1cU7YenSn8mOLHd84wMS4PkMGCoC	ADMIN	t	2026-07-21 07:02:59.79327	$2b$12$wzUxaIXSt02x81afK/7OJuXkPXh5b0TucDNXqT6KMPFIEO1fFa1mq
\.


--
-- Name: alarm_events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.alarm_events_id_seq', 1, false);


--
-- Name: car_plates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.car_plates_id_seq', 1, false);


--
-- Name: devices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.devices_id_seq', 1, false);


--
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- Name: sensor_readings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.sensor_readings_id_seq', 1, false);


--
-- Name: sensors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.sensors_id_seq', 1, false);


--
-- Name: settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.settings_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: alarm
--

SELECT pg_catalog.setval('public.users_id_seq', 2, true);


--
-- Name: alarm_events alarm_events_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.alarm_events
    ADD CONSTRAINT alarm_events_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: car_plates car_plates_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.car_plates
    ADD CONSTRAINT car_plates_pkey PRIMARY KEY (id);


--
-- Name: devices devices_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.devices
    ADD CONSTRAINT devices_pkey PRIMARY KEY (id);


--
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- Name: sensor_readings sensor_readings_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.sensor_readings
    ADD CONSTRAINT sensor_readings_pkey PRIMARY KEY (id);


--
-- Name: sensors sensors_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.sensors
    ADD CONSTRAINT sensors_pkey PRIMARY KEY (id);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_alarm_events_device_id; Type: INDEX; Schema: public; Owner: alarm
--

CREATE INDEX ix_alarm_events_device_id ON public.alarm_events USING btree (device_id);


--
-- Name: ix_alarm_events_timestamp; Type: INDEX; Schema: public; Owner: alarm
--

CREATE INDEX ix_alarm_events_timestamp ON public.alarm_events USING btree ("timestamp");


--
-- Name: ix_alarm_events_user_id; Type: INDEX; Schema: public; Owner: alarm
--

CREATE INDEX ix_alarm_events_user_id ON public.alarm_events USING btree (user_id);


--
-- Name: ix_car_plates_plate_number; Type: INDEX; Schema: public; Owner: alarm
--

CREATE UNIQUE INDEX ix_car_plates_plate_number ON public.car_plates USING btree (plate_number);


--
-- Name: ix_devices_name; Type: INDEX; Schema: public; Owner: alarm
--

CREATE UNIQUE INDEX ix_devices_name ON public.devices USING btree (name);


--
-- Name: ix_notifications_timestamp; Type: INDEX; Schema: public; Owner: alarm
--

CREATE INDEX ix_notifications_timestamp ON public.notifications USING btree ("timestamp");


--
-- Name: ix_notifications_user_id; Type: INDEX; Schema: public; Owner: alarm
--

CREATE INDEX ix_notifications_user_id ON public.notifications USING btree (user_id);


--
-- Name: ix_sensor_readings_sensor_id; Type: INDEX; Schema: public; Owner: alarm
--

CREATE INDEX ix_sensor_readings_sensor_id ON public.sensor_readings USING btree (sensor_id);


--
-- Name: ix_sensor_readings_timestamp; Type: INDEX; Schema: public; Owner: alarm
--

CREATE INDEX ix_sensor_readings_timestamp ON public.sensor_readings USING btree ("timestamp");


--
-- Name: ix_sensors_name; Type: INDEX; Schema: public; Owner: alarm
--

CREATE UNIQUE INDEX ix_sensors_name ON public.sensors USING btree (name);


--
-- Name: ix_settings_key; Type: INDEX; Schema: public; Owner: alarm
--

CREATE UNIQUE INDEX ix_settings_key ON public.settings USING btree (key);


--
-- Name: ix_users_username; Type: INDEX; Schema: public; Owner: alarm
--

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);


--
-- Name: alarm_events alarm_events_device_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.alarm_events
    ADD CONSTRAINT alarm_events_device_id_fkey FOREIGN KEY (device_id) REFERENCES public.devices(id);


--
-- Name: alarm_events alarm_events_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.alarm_events
    ADD CONSTRAINT alarm_events_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: sensor_readings sensor_readings_sensor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: alarm
--

ALTER TABLE ONLY public.sensor_readings
    ADD CONSTRAINT sensor_readings_sensor_id_fkey FOREIGN KEY (sensor_id) REFERENCES public.sensors(id);


--
-- PostgreSQL database dump complete
--

\unrestrict IKEcM39LgMmhSvt6a8yEhKSpzB32M4aRgwmfdMAkradeE6PmxahdJt6ZA84zKR6

