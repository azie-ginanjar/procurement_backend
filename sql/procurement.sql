--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: userid; Type: SEQUENCE; Schema: public; Owner: dev
--

CREATE SEQUENCE userid
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE userid OWNER TO dev;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_users; Type: TABLE; Schema: public; Owner: dev; Tablespace: 
--

CREATE TABLE auth_users (
    id integer DEFAULT nextval('userid'::regclass) NOT NULL,
    username character varying(25) NOT NULL,
    password character varying(256) NOT NULL,
    CONSTRAINT auth_users_password_check CHECK (((password)::text <> ''::text)),
    CONSTRAINT auth_users_username_check CHECK (((username)::text <> ''::text))
);


ALTER TABLE auth_users OWNER TO dev;

--
-- Data for Name: auth_users; Type: TABLE DATA; Schema: public; Owner: dev
--

COPY auth_users (id, username, password) FROM stdin;
2	admin	admin102
\.


--
-- Name: userid; Type: SEQUENCE SET; Schema: public; Owner: dev
--

SELECT pg_catalog.setval('userid', 2, true);


--
-- Name: auth_users_pkey; Type: CONSTRAINT; Schema: public; Owner: dev; Tablespace: 
--

ALTER TABLE ONLY auth_users
    ADD CONSTRAINT auth_users_pkey PRIMARY KEY (id);


--
-- Name: public; Type: ACL; Schema: -; Owner: dev
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM dev;
GRANT ALL ON SCHEMA public TO dev;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

