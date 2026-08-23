--
-- PostgreSQL database dump
--

\restrict 6ZCvtbLS7kBCeXI6EvT67CiP34iSolYO02EmTQiODwoL85xaAuL2WPsAxBjY5BB

-- Dumped from database version 16.14 (Debian 16.14-1.pgdg13+1)
-- Dumped by pg_dump version 16.14 (Debian 16.14-1.pgdg13+1)

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
-- Name: adminrole; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.adminrole AS ENUM (
    'SUPER',
    'MANAGER',
    'TEAM'
);


ALTER TYPE public.adminrole OWNER TO admin;

--
-- Name: profittype; Type: TYPE; Schema: public; Owner: admin
--

CREATE TYPE public.profittype AS ENUM (
    'FIXED',
    'PERCENTAGE'
);


ALTER TYPE public.profittype OWNER TO admin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.admin (
    name character varying NOT NULL,
    email character varying NOT NULL,
    role public.adminrole NOT NULL,
    is_active boolean NOT NULL,
    is_verified boolean NOT NULL,
    id uuid NOT NULL,
    hashed_password character varying NOT NULL,
    last_login timestamp without time zone,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.admin OWNER TO admin;

--
-- Name: service_price; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.service_price (
    service_identifier character varying NOT NULL,
    profit_type public.profittype NOT NULL,
    profit_value double precision NOT NULL,
    id uuid NOT NULL
);


ALTER TABLE public.service_price OWNER TO admin;

--
-- Name: ticket; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.ticket (
    subject character varying NOT NULL,
    priority character varying NOT NULL,
    status character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL,
    id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.ticket OWNER TO admin;

--
-- Name: ticket_message; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.ticket_message (
    message character varying NOT NULL,
    created_at timestamp without time zone NOT NULL,
    is_admin boolean NOT NULL,
    id uuid NOT NULL,
    ticket_id uuid NOT NULL,
    sender_id uuid,
    admin_id uuid
);


ALTER TABLE public.ticket_message OWNER TO admin;

--
-- Name: transaction; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.transaction (
    amount double precision NOT NULL,
    type character varying NOT NULL,
    status character varying NOT NULL,
    reference character varying NOT NULL,
    service_type character varying,
    meta_data character varying,
    profit double precision NOT NULL,
    created_at timestamp without time zone NOT NULL,
    id uuid NOT NULL,
    trans_id character varying,
    wallet_id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.transaction OWNER TO admin;

--
-- Name: user; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public."user" (
    email character varying NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    is_verified boolean NOT NULL,
    full_name character varying,
    id uuid NOT NULL,
    hashed_password character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO admin;

--
-- Name: user_profile; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.user_profile (
    full_name character varying,
    phone_number character varying,
    address character varying,
    state character varying,
    lga character varying,
    nin character varying,
    bvn character varying,
    id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.user_profile OWNER TO admin;

--
-- Name: wallet; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.wallet (
    balance double precision NOT NULL,
    currency character varying NOT NULL,
    id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.wallet OWNER TO admin;

--
-- Data for Name: admin; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.admin (name, email, role, is_active, is_verified, id, hashed_password, last_login, created_at, updated_at) FROM stdin;
samuel dawodu	adoxop1@gmail.com	SUPER	t	f	59997d64-5ff9-4c5e-9bd6-1d57eccc0283	$2b$12$ArOVmonFUWT/474Xzk6ByOVetP8crvZXotyoACPkct9cmECTX/49G	2026-06-15 22:58:58.11641	2026-05-31 10:44:16.474684	2026-05-31 10:44:16.474727
Izunna Nwaikwu	izunna007@gmail.com	SUPER	t	f	a8ea7d02-5520-4e2a-ab3d-2a6daf54cede	$2b$12$bvECp9x1102Tqp0L5C25S.gSusJZvcwOPQ2mjeGa23qpxxXRzLsO2	2026-07-10 17:26:40.240393	2026-06-01 00:25:01.583401	2026-06-01 00:25:01.583459
\.


--
-- Data for Name: service_price; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.service_price (service_identifier, profit_type, profit_value, id) FROM stdin;
\.


--
-- Data for Name: ticket; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.ticket (subject, priority, status, created_at, updated_at, id, user_id) FROM stdin;
Payment 	high	closed	2026-07-06 13:00:02.234416	2026-07-06 19:54:19.305053	3a698251-9998-4174-8692-8c44370f527e	f0ba467e-f24c-46fe-87a4-2e8d27946b80
My payment is not reflecting 	medium	open	2026-07-09 12:27:10.335734	2026-07-09 13:23:31.616801	4dff654d-fbf5-437a-b343-e24c8c9878b7	2221b6a6-c5a2-40e3-af65-25bcebb9daa0
My payment is not reflecting after using transfer with opay	medium	open	2026-07-09 15:35:33.893709	2026-07-09 15:35:33.893728	89274548-34fe-451c-98f8-276714bcfd00	2221b6a6-c5a2-40e3-af65-25bcebb9daa0
Payment successful but not in balance 	high	open	2026-07-23 21:12:52.028152	2026-07-24 23:07:30.647231	c0329ae0-63fe-410b-815d-70fa245a9db3	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0
Payment successful but not in balance 	high	open	2026-07-26 07:39:11.62085	2026-07-26 07:39:11.62088	31f6aff2-049d-4106-b0ef-2b8fcd8cd015	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0
\.


--
-- Data for Name: ticket_message; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.ticket_message (message, created_at, is_admin, id, ticket_id, sender_id, admin_id) FROM stdin;
I have funded my wallet yet it not allowing me to fund my Sltv	2026-07-06 13:00:02.286737	f	6a661061-e76f-4b70-84ad-e848b026b2f3	3a698251-9998-4174-8692-8c44370f527e	f0ba467e-f24c-46fe-87a4-2e8d27946b80	\N
Even to buy data i cannot what is going on 	2026-07-06 13:00:45.068496	f	94c5f573-a9b7-41e7-9c7c-43620ea1f4d4	3a698251-9998-4174-8692-8c44370f527e	f0ba467e-f24c-46fe-87a4-2e8d27946b80	\N
The SLTV subscription is working now	2026-07-06 19:54:19.298315	t	c2782a49-2006-4b5e-b7b3-3ed6dd3f04e0	3a698251-9998-4174-8692-8c44370f527e	\N	a8ea7d02-5520-4e2a-ab3d-2a6daf54cede
I made a payment of 5000 naira to PAYSTACK-TITAN | 9981093091  few minutes ago, using my Opay 901 3526 714 and its not reflecting in my wallet 	2026-07-09 12:27:10.352088	f	9bf55768-5aa0-41ad-9823-045f1d84183d	4dff654d-fbf5-437a-b343-e24c8c9878b7	2221b6a6-c5a2-40e3-af65-25bcebb9daa0	\N
Noted, it will be refunded, but for now, don't do transfer, pay directly with opay	2026-07-09 13:23:31.609015	t	fdafff4d-e354-4d32-9757-cebd156ea565	4dff654d-fbf5-437a-b343-e24c8c9878b7	\N	a8ea7d02-5520-4e2a-ab3d-2a6daf54cede
My payment transfer of 5000 using paystack transfer with opay\nTransaction Details\n\nMerchant Name : paystack Payment Limited \nPayment Method: Wallet \nTransaction Date: Jul 9th, 2026 15:12:24\n\nTransaction No.\n260709140300376911709368\n\nMerchant Order No.\n\npaystack_6342416319_1jpy7\n\nIts still not reflecting in my wallet	2026-07-09 15:35:33.900307	f	ff521cd6-0e1f-47cb-bc92-c2ad152ed4a1	89274548-34fe-451c-98f8-276714bcfd00	2221b6a6-c5a2-40e3-af65-25bcebb9daa0	\N
I funded my account via Opay transfer on paystack and it was successful but I couldn’t get the balance on my wallet	2026-07-23 21:12:52.072914	f	805668ea-694e-4f8c-ba98-174ad2408809	c0329ae0-63fe-410b-815d-70fa245a9db3	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0	\N
Hello	2026-07-24 23:07:30.594552	f	8c04b018-fe23-4b78-9899-ed2a9e70b337	c0329ae0-63fe-410b-815d-70fa245a9db3	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0	\N
I top up my account with 5,000 via paystack Opay transfer and it was successful but I didn’t get the fund in my wallet balance 	2026-07-26 07:39:11.675811	f	f5dae4a7-705b-4566-9e14-cf21d79c11aa	31f6aff2-049d-4106-b0ef-2b8fcd8cd015	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0	\N
\.


--
-- Data for Name: transaction; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.transaction (amount, type, status, reference, service_type, meta_data, profit, created_at, id, trans_id, wallet_id, user_id) FROM stdin;
5000	credit	success	T751492849560624	funding	Paystack Funding	0	2026-06-15 22:30:45.885664	b3de37b4-0815-4362-a4e2-aa11d2e3521b	260615223045HSG	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
5000	debit	success	TV-26de5ccb-ad77-4ce8-9cd5-59ded920f7da-SB101240601133	tv	Provider: sltv | Local Automation Result: Success (Message not captured)	0	2026-06-15 22:31:40.782881	3394b9f2-3c7e-445f-a56b-e462e1129775	260615223140PWY	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
5000	credit	success	T576654378252352	funding	Paystack Funding	0	2026-06-23 09:43:14.365077	0b8b823e-9397-4f4b-a495-0299e065168f	260623094314ZMZ	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
5000	debit	success	TV-26de5ccb-ad77-4ce8-9cd5-59ded920f7da-SB201162024	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-23 19:15:51.865001	75128a42-b2ab-4656-a06e-44a260a236ec	260623191551ZX6	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
10000	credit	success	T395965012854439	funding	Paystack Funding	0	2026-06-24 12:44:28.74168	ba8a00c4-17a6-4f75-b5c0-f3fdd431fd11	2606241244287MK	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-Sn201269017	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-06-24 14:11:30.966164	b51a9430-82ed-43ae-a17b-fb91c20f6181	2606241411305EU	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-b51a9430-82ed-43ae-a17b-fb91c20f6181	refund	Refund for failed TV transaction b51a9430-82ed-43ae-a17b-fb91c20f6181	0	2026-06-24 14:12:00.112787	780603a0-57a5-4a97-aa62-e5a59f34d52c	2606241412006GM	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-Sn201269017	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-06-24 14:13:24.408084	dd144e06-1d31-4ff1-968f-f402c2ddbf71	260624141324HEL	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-dd144e06-1d31-4ff1-968f-f402c2ddbf71	refund	Refund for failed TV transaction dd144e06-1d31-4ff1-968f-f402c2ddbf71	0	2026-06-24 14:13:55.838767	f4ba558f-8e01-4dbb-a59d-98058f8cb4c7	260624141355WJA	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401004007	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-24 17:19:38.123337	374c7204-ed61-458c-9f38-08f35b720cb9	260624171938ZV1	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T162612523452569	funding	Paystack Funding	0	2026-06-25 12:46:17.55968	650e99b1-f992-492b-8e7a-b9a5a4a23db4	260625124617X3O	d6690f92-b426-4465-8d56-90768d5d981c	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0
5000	debit	success	TV-d6690f92-b426-4465-8d56-90768d5d981c-SB101240601755	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-25 12:46:31.486307	1ee98c14-6805-4343-adf5-62611c42beb4	26062512463169V	d6690f92-b426-4465-8d56-90768d5d981c	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0
40000	credit	success	T636465599994175	funding	Paystack Funding	0	2026-06-26 03:59:19.578708	813c5a2c-42c4-4f8f-a835-be1f0db46997	260626035919DT6	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101240601592	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 04:00:42.730119	5f307502-c580-4f9d-adb0-94aac36901db	260626040042G1Y	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201014698	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 04:10:25.091471	c9fcf90a-2b74-4dd9-b188-15aa78738aa7	260626041025XTI	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201014698	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 04:11:26.170567	62a8a518-48f5-4b15-9f21-f34e21930969	260626041126FRM	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201014698	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 04:11:43.329711	bfb18eb0-4695-41d0-aa57-18cb5b8b59a9	260626041143Y9S	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201014698	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 04:11:58.413316	8f8f0231-250b-45e3-a432-370888fda918	260626041158RT8	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201014698	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 04:13:57.368772	308a763b-90d9-41be-898f-3dcb91cf1824	26062604135746I	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201203155	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 06:47:12.656076	24bce7b2-94fa-451e-9db9-9ea268af99a0	260626064712CTJ	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101240600081	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-26 13:01:27.038556	27712b02-04a8-4cef-93ff-d465f6a52730	260626130127F9X	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
20000	credit	success	T035136763817397	funding	Paystack Funding	0	2026-06-26 13:06:59.612046	5cafd1d9-3e8b-4841-8735-8eca6836993b	26062613065958Z	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T063485365279569	funding	Paystack Funding	0	2026-06-26 18:07:33.922017	55676fd9-d47d-4777-b1ad-86f1008153d0	260626180733J52	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401035607	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-27 08:12:41.524128	ba332c9b-8608-4760-97f2-9b1a53fbaa4a	260627081241C7E	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401035638	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-27 08:16:32.574389	6c427b8a-46fe-4ada-9641-c150ba65fb1d	260627081632G7B	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB301241113042	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-27 16:17:37.739191	be694251-34e7-4ad6-bd00-c5559ad890a1	2606271617374W0	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201107851	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-27 20:35:40.560289	af7f155d-8979-4dc3-989d-95f2db30647a	2606272035404W9	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201107851	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-27 20:35:57.560133	cac4207a-3086-4e47-8712-d3f7ca21b423	260627203557J9A	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
20000	credit	success	T917956174348157	funding	Paystack Funding	0	2026-06-27 20:45:04.97794	b7be87ee-f900-4d3e-90f7-31b5c430dd26	260627204504WR5	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101240600314	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-27 20:47:16.615131	78ee77f1-4450-4c31-8cc3-6c7ef4836c21	260627204716FRW	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T571184183663713	funding	Paystack Funding	0	2026-06-28 06:37:48.192445	b66bd9f2-c2a9-4532-96a5-be1dca7e8c10	260628063748J0W	c9368e77-b726-4d65-b8e8-1a4fb6e16195	89b5793a-59ab-4f04-af43-3b9991f7f82f
5000	debit	success	TV-c9368e77-b726-4d65-b8e8-1a4fb6e16195-SB301241103294	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-28 06:38:21.494436	5eecc33a-5aa9-420b-81e3-9a83c4104bc3	260628063821Z3F	c9368e77-b726-4d65-b8e8-1a4fb6e16195	89b5793a-59ab-4f04-af43-3b9991f7f82f
15000	credit	success	T789392503336666	funding	Paystack Funding	0	2026-06-28 06:58:37.963439	70220c08-948d-4ed6-86c7-942fdb7442a7	260628065837TWZ	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201113299	tv	Provider: sltv | Local Automation Result: Do not have sufficient balance	0	2026-06-28 06:59:01.04064	69af49ec-0a2c-451c-b954-d06d9723005b	260628065901B5U	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201019638	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-28 20:42:15.078662	232a3ef3-6ea9-4715-80d7-b999fc12cefd	260628204215C84	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101231017771	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-30 16:32:23.536976	de69e7b1-23bf-48b6-b0bc-66db082f9e4f	260630163223OK5	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401010062	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-30 20:22:20.02228	add41085-7f05-4d81-af8a-27d2c1105b7e	260630202220RNX	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T065169724180536	funding	Paystack Funding	0	2026-06-30 21:37:14.284712	ec7a8485-f279-499c-8e9e-166418c2cbcf	2606302137149K2	2c1662ff-e025-4f30-9d21-b9b5efc16ff7	2221b6a6-c5a2-40e3-af65-25bcebb9daa0
5000	debit	success	TV-2c1662ff-e025-4f30-9d21-b9b5efc16ff7-SB201205796	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-06-30 21:37:34.44585	ef22cb5e-418b-4af9-91fd-25ebec4c3334	260630213734Y27	2c1662ff-e025-4f30-9d21-b9b5efc16ff7	2221b6a6-c5a2-40e3-af65-25bcebb9daa0
10000	credit	success	T748338914125755	funding	Paystack Funding	0	2026-07-01 18:48:08.472577	de035813-2a35-49c3-80a7-e8b0f4646c7b	2607011848088U3	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB301241104783	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-01 18:48:42.481667	25f0103f-54e3-4b94-865f-8b0af7c69b44	260701184842HKZ	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101045096	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-01 18:50:10.87469	633caa18-7734-4528-a898-aa8c9b4f11d3	260701185010QNP	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401014186	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-02 16:41:31.195933	b901e4aa-67fe-4535-87d9-c2778e1f7de5	260702164131OL5	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-02 17:43:15.466649	bf256d5e-1597-4fe7-87ed-ffffdaf40118	260702174315ZU9	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-bf256d5e-1597-4fe7-87ed-ffffdaf40118	refund	Refund for failed TV transaction bf256d5e-1597-4fe7-87ed-ffffdaf40118	0	2026-07-02 17:43:20.90058	a1324993-fcf7-4ac6-b519-a572fd253b3a	260702174320FJD	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-02 17:43:42.231983	6fdb6c21-b2c3-485f-b33e-74b7259581a0	2607021743425KS	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-6fdb6c21-b2c3-485f-b33e-74b7259581a0	refund	Refund for failed TV transaction 6fdb6c21-b2c3-485f-b33e-74b7259581a0	0	2026-07-02 17:43:47.641578	2ed9ea3e-5299-4aa2-9547-664c12fbcf9b	2607021743478UN	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T404056762754835	funding	Paystack Funding	0	2026-07-02 19:12:19.769881	fef6f9bf-34bd-47b1-9cb3-afc549045c78	26070219121932A	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201204131	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-02 19:14:56.651988	b20d899c-8681-46f9-b7e6-237e9d5c5066	260702191456Z5Q	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-02 20:01:20.838301	bdfcc3a8-e702-42eb-92de-44a21de40d93	26070220012047R	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-bdfcc3a8-e702-42eb-92de-44a21de40d93	refund	Refund for failed TV transaction bdfcc3a8-e702-42eb-92de-44a21de40d93	0	2026-07-02 20:01:26.075212	1afcc02a-c457-471d-8771-93f852d4b48c	260702200126X9Q	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 05:59:17.846807	823b8769-bccf-4bc1-bf92-2d1504dc9110	2607030559176XA	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-823b8769-bccf-4bc1-bf92-2d1504dc9110	refund	Refund for failed TV transaction 823b8769-bccf-4bc1-bf92-2d1504dc9110	0	2026-07-03 05:59:23.124709	b1830e25-a5ab-4ef4-9cef-0a4bf16648fc	2607030559233BS	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 05:59:34.157859	a6820a6f-899d-442c-8439-4deaf6bc0dc6	26070305593411E	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-a6820a6f-899d-442c-8439-4deaf6bc0dc6	refund	Refund for failed TV transaction a6820a6f-899d-442c-8439-4deaf6bc0dc6	0	2026-07-03 05:59:39.443038	ae249a70-5bf4-46e8-afb9-8e90323e2f48	260703055939VSJ	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 05:59:46.04995	e11b7b87-4d53-441b-9624-1d85de2d1ece	260703055946R30	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-e11b7b87-4d53-441b-9624-1d85de2d1ece	refund	Refund for failed TV transaction e11b7b87-4d53-441b-9624-1d85de2d1ece	0	2026-07-03 05:59:51.38957	213dad4f-2259-4383-92b5-dab9910e3e23	260703055951LG9	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 10:16:34.462317	c52919ab-d923-4e52-901a-6e3d02298626	260703101634NWR	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-c52919ab-d923-4e52-901a-6e3d02298626	refund	Refund for failed TV transaction c52919ab-d923-4e52-901a-6e3d02298626	0	2026-07-03 10:16:39.546755	5f3ee107-86f3-4d83-a3e0-0a0c3fdc15f5	260703101639V3W	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 14:02:17.570428	e5b41087-a5ac-4550-8cff-9681eca1b429	2607031402176F4	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-e5b41087-a5ac-4550-8cff-9681eca1b429	refund	Refund for failed TV transaction e5b41087-a5ac-4550-8cff-9681eca1b429	0	2026-07-03 14:02:22.819408	3c9da4ca-f6fd-468d-b05a-9fad362a94c7	260703140222E4B	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 14:02:30.533985	933a19c9-db07-46db-aec4-9b2c53811349	260703140230RWV	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-933a19c9-db07-46db-aec4-9b2c53811349	refund	Refund for failed TV transaction 933a19c9-db07-46db-aec4-9b2c53811349	0	2026-07-03 14:02:36.157561	a0fbb36e-de5d-4e6d-9934-474f66f5ccd7	260703140236UI9	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-26de5ccb-ad77-4ce8-9cd5-59ded920f7da-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 14:34:22.936104	bc05dfe2-f688-469e-9926-1e2758297f14	260703143422NUS	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
5000	credit	success	REFUND-bc05dfe2-f688-469e-9926-1e2758297f14	refund	Refund for failed TV transaction bc05dfe2-f688-469e-9926-1e2758297f14	0	2026-07-03 14:34:28.248998	2b9fb7da-0e7c-47d9-b959-9f4169e883dd	260703143428Q8R	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 18:34:17.227973	bf7f1939-d77b-497c-9e98-d11fe329e4c0	260703183417MD1	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-bf7f1939-d77b-497c-9e98-d11fe329e4c0	refund	Refund for failed TV transaction bf7f1939-d77b-497c-9e98-d11fe329e4c0	0	2026-07-03 18:34:23.008164	71083776-9c73-4d42-b8ac-e3a8d7a95807	260703183423D4H	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 18:34:32.588322	52314870-2225-4c08-b097-7c1977bc1476	260703183432KCV	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-52314870-2225-4c08-b097-7c1977bc1476	refund	Refund for failed TV transaction 52314870-2225-4c08-b097-7c1977bc1476	0	2026-07-03 18:34:37.710115	0ca6d50c-e5c3-4af1-97a8-030d89b16450	260703183437AB4	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 18:34:50.840643	551237ae-f3cb-4ec9-8595-bba472e31c34	260703183450TS0	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-551237ae-f3cb-4ec9-8595-bba472e31c34	refund	Refund for failed TV transaction 551237ae-f3cb-4ec9-8595-bba472e31c34	0	2026-07-03 18:34:56.221247	481f3536-4b4e-4c32-bfeb-c0b9e7984959	2607031834566JC	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-03 21:28:20.704059	ad940510-fc77-4690-b8bf-e9fbb94e9b83	260703212820Y48	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-ad940510-fc77-4690-b8bf-e9fbb94e9b83	refund	Refund for failed TV transaction ad940510-fc77-4690-b8bf-e9fbb94e9b83	0	2026-07-03 21:28:25.648889	0ed52c3c-42ad-4bd9-bf6a-cdae31eebda7	260703212825DGH	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 08:06:07.472254	1ef0d85c-edd8-41c4-a96b-bcb70b0884a0	2607040806072FH	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-1ef0d85c-edd8-41c4-a96b-bcb70b0884a0	refund	Refund for failed TV transaction 1ef0d85c-edd8-41c4-a96b-bcb70b0884a0	0	2026-07-04 08:06:13.032449	9d156776-0591-4e89-97ff-f1c4672a33a1	260704080613RAK	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 08:07:14.976581	dcc91ef8-7ae5-4b61-a3bb-6921f0f8b41a	2607040807142W2	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-dcc91ef8-7ae5-4b61-a3bb-6921f0f8b41a	refund	Refund for failed TV transaction dcc91ef8-7ae5-4b61-a3bb-6921f0f8b41a	0	2026-07-04 08:07:23.217555	13f3a8e5-c9ad-4a9c-b09e-3f17ea4ef11f	260704080723NPA	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 08:08:49.850044	863a8837-8d61-496a-980e-e20e4b099738	2607040808496XX	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-863a8837-8d61-496a-980e-e20e4b099738	refund	Refund for failed TV transaction 863a8837-8d61-496a-980e-e20e4b099738	0	2026-07-04 08:08:55.375023	6d33ee64-6285-4dd4-adf6-ef9222caeb11	260704080855U83	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101231004245	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-04 12:28:58.05618	50c09dd4-7ae4-4c55-8b42-6effc107dd0f	260704122858TL9	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T362729701949757	funding	Paystack Funding	0	2026-07-04 12:52:37.340564	c661af14-05d2-45f3-a922-11943830ba71	260704125237VNK	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101013699	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-04 12:53:26.048904	2a859956-adff-4339-9037-f11b353e7ab3	260704125326D62	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T232361458873012	funding	Paystack Funding	0	2026-07-04 13:19:24.673478	0c2acbae-b65c-4123-a0ec-b8259e87618a	260704131924H8U	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:21:46.020998	a07a59d0-cb4b-48cb-92e4-46c65e984936	2607041321466QX	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-a07a59d0-cb4b-48cb-92e4-46c65e984936	refund	Refund for failed TV transaction a07a59d0-cb4b-48cb-92e4-46c65e984936	0	2026-07-04 13:21:51.367623	d6d89528-63fa-458e-b885-ba06b1a27233	260704132151Q5W	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:22:20.521524	3f5eb651-d081-4ca9-9782-9e4f41dcb472	2607041322206C3	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-3f5eb651-d081-4ca9-9782-9e4f41dcb472	refund	Refund for failed TV transaction 3f5eb651-d081-4ca9-9782-9e4f41dcb472	0	2026-07-04 13:22:25.892474	081a09a2-dcc1-45c7-ac0e-b6ff1ca9fae4	260704132225DP4	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:24:20.808531	d40f5bc2-8e97-4032-b7d9-c1c0e839d3c5	260704132420OER	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-d40f5bc2-8e97-4032-b7d9-c1c0e839d3c5	refund	Refund for failed TV transaction d40f5bc2-8e97-4032-b7d9-c1c0e839d3c5	0	2026-07-04 13:24:26.022874	ede6979a-6cb7-42c9-8786-d59ddcee36be	260704132426DT9	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:24:34.629274	76585ec1-253b-4860-bc43-cea9da2c393d	260704132434HJY	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-76585ec1-253b-4860-bc43-cea9da2c393d	refund	Refund for failed TV transaction 76585ec1-253b-4860-bc43-cea9da2c393d	0	2026-07-04 13:24:39.896253	2c534638-d90a-4189-abe0-f1e60a25889a	260704132439FYG	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:24:43.150947	d6f07b4a-78b0-4401-bc32-301ee7c928bf	260704132443GOL	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-d6f07b4a-78b0-4401-bc32-301ee7c928bf	refund	Refund for failed TV transaction d6f07b4a-78b0-4401-bc32-301ee7c928bf	0	2026-07-04 13:24:48.10989	5f1e403a-09c1-47d6-9697-31ac20294de3	260704132448DU4	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:24:58.136102	c81bc95f-a228-4260-8f81-b48b694d1634	260704132458DUR	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-c81bc95f-a228-4260-8f81-b48b694d1634	refund	Refund for failed TV transaction c81bc95f-a228-4260-8f81-b48b694d1634	0	2026-07-04 13:25:03.562513	3dd707f6-fcad-4455-b45b-ace481e895ce	2607041325032Q5	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:37:15.959441	7f8c98fd-1e4e-453f-af66-f3895f8a2d33	260704133715BZG	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-7f8c98fd-1e4e-453f-af66-f3895f8a2d33	refund	Refund for failed TV transaction 7f8c98fd-1e4e-453f-af66-f3895f8a2d33	0	2026-07-04 13:37:21.332594	0a2d7265-abad-49f7-9c3c-5a6ff706febb	260704133721ZAG	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:37:31.388004	bfc76699-8586-48e1-9215-f65c31907622	260704133731N24	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-bfc76699-8586-48e1-9215-f65c31907622	refund	Refund for failed TV transaction bfc76699-8586-48e1-9215-f65c31907622	0	2026-07-04 13:37:36.66962	573c497c-c3dd-44d6-bdb4-bfa2b79a7da1	260704133736HLG	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-fd64af6d-83b0-41d3-9746-82eb30560adb	refund	Refund for failed TV transaction fd64af6d-83b0-41d3-9746-82eb30560adb	0	2026-07-04 13:45:03.972805	230cb27c-e0b2-4676-bed2-cd0f9e8e2048	2607041345037F0	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:45:05.691451	602f65a0-c071-4787-b153-76be031bdaaa	260704134505CAP	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-602f65a0-c071-4787-b153-76be031bdaaa	refund	Refund for failed TV transaction 602f65a0-c071-4787-b153-76be031bdaaa	0	2026-07-04 13:45:10.578287	9ea2c87f-c5bc-48bf-a5c0-75897fa32ddb	2607041345100I1	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:45:16.374646	b60c9a00-8fbd-496a-a085-eeeec96cde96	260704134516Z55	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-b60c9a00-8fbd-496a-a085-eeeec96cde96	refund	Refund for failed TV transaction b60c9a00-8fbd-496a-a085-eeeec96cde96	0	2026-07-04 13:45:21.712982	81978a5e-1ab9-425b-af39-475a207d4fd6	260704134521BQV	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:44:40.969023	745815c1-249c-452b-91ae-2b16eaa4a599	260704134440X88	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-745815c1-249c-452b-91ae-2b16eaa4a599	refund	Refund for failed TV transaction 745815c1-249c-452b-91ae-2b16eaa4a599	0	2026-07-04 13:44:46.266487	4de89b89-37d3-494d-a565-a97342f6b5ef	260704134446DMO	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101009461	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-04 13:44:58.566364	fd64af6d-83b0-41d3-9746-82eb30560adb	2607041344589Y3	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101046198	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-04 13:52:37.099462	a6a84763-ac79-4d7d-be9c-cf40ffdca794	2607041352376PI	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T871441580408844	funding	Paystack Funding	0	2026-07-04 16:10:56.281117	6bf2e54f-abc6-467f-9af5-330cb4ddb573	260704161056WQK	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401021630	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-04 16:11:24.715756	7f56dfe3-30b9-4085-a8f3-cf0b59c97628	260704161124YFB	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T843256667416623	funding	Paystack Funding	0	2026-07-06 06:35:46.188336	714ec8c4-e804-4361-9b70-decd63d8be69	260706063546T7Y	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301024110590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 06:38:58.95922	ddd5afde-94aa-4582-9494-6c1f535bf3e4	260706063858ANP	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-ddd5afde-94aa-4582-9494-6c1f535bf3e4	refund	Refund for failed TV transaction ddd5afde-94aa-4582-9494-6c1f535bf3e4	0	2026-07-06 06:39:34.681113	1a5b3229-4ef0-42d6-884d-228b2f81c10c	2607060639344O1	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301024110590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 06:39:42.091277	f3d368f4-a3ad-4368-a305-78fc75991eb5	260706063942AZU	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-f3d368f4-a3ad-4368-a305-78fc75991eb5	refund	Refund for failed TV transaction f3d368f4-a3ad-4368-a305-78fc75991eb5	0	2026-07-06 06:40:17.67577	1c9fcbb3-3fd6-47da-9909-5c129bfc4e10	260706064017PVF	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301024110590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 06:46:53.267287	25c47f3d-0dce-44fe-a720-9e3e641ead91	260706064653XH6	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-25c47f3d-0dce-44fe-a720-9e3e641ead91	refund	Refund for failed TV transaction 25c47f3d-0dce-44fe-a720-9e3e641ead91	0	2026-07-06 06:47:28.275933	4d676abd-6b3a-4557-896e-3b9bb75212bf	260706064728JOK	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
7000	credit	success	T320758550579220	funding	Paystack Funding	0	2026-07-06 06:57:39.281534	686919b9-6a9c-4d19-93a8-6defe94609f3	260706065739J3Y	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401034350	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-06 06:58:41.679379	954f5185-64db-4bba-82d3-4b4a2357ece1	2607060658418CJ	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301241101590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 09:35:59.106935	884fb569-17c4-446c-bf76-806a854a4f4b	260706093559DFB	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-884fb569-17c4-446c-bf76-806a854a4f4b	refund	Refund for failed TV transaction 884fb569-17c4-446c-bf76-806a854a4f4b	0	2026-07-06 09:36:31.699939	27e54fc7-13d1-44cb-8698-8b63ec9d2316	260706093631L6R	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
200	credit	success	T556918518455937	funding	Paystack Funding	0	2026-07-06 09:38:59.380709	a29effb5-b293-4369-96c5-218287028d73	260706093859AA4	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301241101590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 09:39:50.778563	53ac25ca-ee13-48b9-b0e1-8f7d7394fb1b	260706093950PY4	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-53ac25ca-ee13-48b9-b0e1-8f7d7394fb1b	refund	Refund for failed TV transaction 53ac25ca-ee13-48b9-b0e1-8f7d7394fb1b	0	2026-07-06 09:40:23.356322	18cdd086-1608-46f6-ae53-75a479dab61f	260706094023VN3	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301241101590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 12:56:32.605244	0047ac43-da99-4657-980a-5bcf9c49fe51	26070612563260X	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-0047ac43-da99-4657-980a-5bcf9c49fe51	refund	Refund for failed TV transaction 0047ac43-da99-4657-980a-5bcf9c49fe51	0	2026-07-06 12:57:07.28122	20b6d2d3-887d-4bc4-8701-0ef3e28e9b14	26070612570707S	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	debit	failed	AIRTIME-30ae425f-efe5-410d-a495-7ff9094c6b02-07012129090	airtime	Network: BAD | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-07-06 12:57:33.219516	d190efc9-6901-43ee-bdb5-574280bd2e30	260706125733W2E	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	credit	success	REFUND-d190efc9-6901-43ee-bdb5-574280bd2e30	refund	Refund for failed Airtime transaction d190efc9-6901-43ee-bdb5-574280bd2e30	0	2026-07-06 12:57:34.158345	6616571a-0011-4bbf-a4b6-038bb830c6f9	2607061257349I2	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	debit	failed	AIRTIME-30ae425f-efe5-410d-a495-7ff9094c6b02-07012129090	airtime	Network: BAD | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-07-06 12:57:41.533296	768c0e7f-ea73-422c-a039-8cd4e99dbe4d	260706125741PQM	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	credit	success	REFUND-768c0e7f-ea73-422c-a039-8cd4e99dbe4d	refund	Refund for failed Airtime transaction 768c0e7f-ea73-422c-a039-8cd4e99dbe4d	0	2026-07-06 12:57:41.998913	1fe314ce-5f94-4325-be5b-ae214f2202e7	260706125741TGJ	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	debit	failed	AIRTIME-30ae425f-efe5-410d-a495-7ff9094c6b02-07012129090	airtime	Network: BAD | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-07-06 13:01:49.631995	eea611e5-1c60-4e13-b6f4-fb7b7bb5d82d	260706130149ZAK	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	credit	success	REFUND-eea611e5-1c60-4e13-b6f4-fb7b7bb5d82d	refund	Refund for failed Airtime transaction eea611e5-1c60-4e13-b6f4-fb7b7bb5d82d	0	2026-07-06 13:01:50.070806	fbe68d25-b5ad-4e66-9b45-f24553b6e055	2607061301505D3	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	success	TV-26de5ccb-ad77-4ce8-9cd5-59ded920f7da-Sb301241113504	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-06 18:03:37.786133	7e26ad27-a519-4833-aeab-9db7a1b4440b	2607061803374K3	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301241101590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 19:58:17.000914	027e4122-17ed-4743-a6a1-2ad7ceb3ee33	260706195817ZVN	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-027e4122-17ed-4743-a6a1-2ad7ceb3ee33	refund	Refund for failed TV transaction 027e4122-17ed-4743-a6a1-2ad7ceb3ee33	0	2026-07-06 19:58:49.956295	bfa978eb-02f0-4144-86f2-d4e75148d9c4	260706195849HEF	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-a0f2f2f7-8382-48d3-a19b-f250c77d6f46	refund	Refund for failed TV transaction a0f2f2f7-8382-48d3-a19b-f250c77d6f46	0	2026-07-06 19:59:54.867399	5d43ca6f-3e46-41bc-8b8b-17a63c553403	2607061959546HX	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301241101590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 19:59:13.617072	a0f2f2f7-8382-48d3-a19b-f250c77d6f46	2607061959131GI	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	T906632842930983	funding	Paystack Funding	0	2026-07-06 20:06:51.168089	d8d58a8a-0627-4afa-a0be-32122dadeacf	26070620065119M	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201203599	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-06 20:08:41.016279	a6853c4b-0bdf-444d-b12d-ea132534e5b7	260706200841XBK	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-ceec2787-1d1b-4292-8316-6e80a5bcd668	refund	Refund for failed TV transaction ceec2787-1d1b-4292-8316-6e80a5bcd668	0	2026-07-06 20:13:02.573429	3b10a945-c083-4746-a559-238f7cd3cfe0	260706201302X2O	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	debit	failed	AIRTIME-30ae425f-efe5-410d-a495-7ff9094c6b02-07012129090	airtime	Network: BAD | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-07-07 16:42:43.403865	e02c0d2c-f8f3-4fe8-99d8-8495ff03374f	260707164243OTB	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	T464013071683835	funding	Paystack Funding	0	2026-07-06 20:10:28.958678	2d749ee2-a89b-4654-9382-035d178f7e6c	260706201028Y6S	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301241101590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 20:10:16.523804	8b8a7d58-7ef8-4591-a4c3-36cfa191a931	260706201016QNZ	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	credit	success	REFUND-8b8a7d58-7ef8-4591-a4c3-36cfa191a931	refund	Refund for failed TV transaction 8b8a7d58-7ef8-4591-a4c3-36cfa191a931	0	2026-07-06 20:10:52.57423	83fff205-2a7e-44ac-b862-ed3c0fe0e2e3	260706201052MWF	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	credit	success	REFUND-e02c0d2c-f8f3-4fe8-99d8-8495ff03374f	refund	Refund for failed Airtime transaction e02c0d2c-f8f3-4fe8-99d8-8495ff03374f	0	2026-07-07 16:42:43.970742	85b5563f-4c58-4545-8c61-e02a46eb1b43	260707164243TBI	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	debit	failed	AIRTIME-30ae425f-efe5-410d-a495-7ff9094c6b02-07012129090	airtime	Network: BAD | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-07-07 16:42:49.601892	48bbe777-6cfd-4e5e-90cc-12358e7b5526	260707164249U74	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	failed	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-301241101590	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-06 20:12:30.022248	ceec2787-1d1b-4292-8316-6e80a5bcd668	2607062012303WB	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201113143	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-06 20:12:34.199375	3c64aa26-a7fd-4eda-bc6c-d13bd180a486	260706201234DFM	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-30ae425f-efe5-410d-a495-7ff9094c6b02-Sb301241101590	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-06 20:16:27.098548	1d962024-b09f-41d0-ae52-e46280c815be	260706201627239	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	credit	success	REFUND-48bbe777-6cfd-4e5e-90cc-12358e7b5526	refund	Refund for failed Airtime transaction 48bbe777-6cfd-4e5e-90cc-12358e7b5526	0	2026-07-07 16:42:50.065548	19143fc6-b537-492e-b892-d804b763a24c	2607071642500GT	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	debit	failed	AIRTIME-30ae425f-efe5-410d-a495-7ff9094c6b02-07012129090	airtime	Network: BAD | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-07-07 16:43:19.180476	4ac9b43b-a3ab-40da-bf35-0e91a0d43b63	260707164319TMM	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	credit	success	REFUND-4ac9b43b-a3ab-40da-bf35-0e91a0d43b63	refund	Refund for failed Airtime transaction 4ac9b43b-a3ab-40da-bf35-0e91a0d43b63	0	2026-07-07 16:43:19.759701	b3d4a5de-1d9e-4583-ac68-94ea44fa25c9	260707164319J6W	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	debit	failed	AIRTIME-30ae425f-efe5-410d-a495-7ff9094c6b02-07012129090	airtime	Network: BAD | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-07-07 17:03:11.865279	705ec248-28ae-425a-8fa5-d29a6ae522c1	260707170311KL4	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
100	credit	success	REFUND-705ec248-28ae-425a-8fa5-d29a6ae522c1	refund	Refund for failed Airtime transaction 705ec248-28ae-425a-8fa5-d29a6ae522c1	0	2026-07-07 17:03:12.407802	3d24999e-2a2e-44d2-a3a2-c9b40dbe84c2	260707170312DCC	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
10000	credit	success	T498345563245314	funding	Paystack Funding	0	2026-07-07 17:57:54.721526	c88bdcdc-c903-4083-bee7-cbfc3d2e0c13	26070717575455M	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
10000	credit	success	T804325078843122	funding	Paystack Funding	0	2026-07-07 17:59:38.965531	e802f293-c516-4837-8bd7-7fb52a4068cd	260707175938L25	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101051516	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-07 18:07:58.001285	6692d980-53b7-4140-83aa-4640ca434aca	260707180758BGL	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
13000	credit	success	T928949158017096	funding	Paystack Funding	0	2026-07-07 18:55:41.778542	81111dc5-597a-4277-8ef0-c4464b2d6032	260707185541UO2	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb301241101215	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-07 18:58:48.015681	abcd9522-e5ee-4036-baad-2bcad04a6bb8	2607071858485V3	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201168572	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-07 19:18:36.294872	3ec766d8-aa68-4627-b606-704a2af334f3	26070719183608N	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401006983	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-07 19:30:56.238913	91de0cf0-7a64-4f87-889a-1aeb87a9f406	260707193056W4C	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T822764031476388	funding	Paystack Funding	0	2026-07-08 15:59:00.922753	cff70dcf-da43-4ac3-9384-16c66e8d3226	260708155900KOG	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T500234506997648	funding	Paystack Funding	0	2026-07-08 18:40:56.93514	67d6a4d8-30ed-4248-be15-ba716bbb60f9	2607081840568ZY	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401006463	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-08 18:41:28.704275	440a7873-f8bf-4bb3-81e1-be9e910b81c4	260708184128PLP	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101051459	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-09 16:45:02.100772	16fec561-62af-42aa-ad88-01b7ce45eaf8	260709164502S1B	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201193357	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-10 12:05:37.014987	1f73fb39-e553-42d4-83f2-428b67e331c6	2607101205376QT	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201112272	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-10 20:13:05.812908	382b7036-be76-4f15-8e4f-bcaaf597caa6	260710201305Z3D	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201211378	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-10 20:36:04.26032	10862ed7-678b-4518-8e72-4900ac59c9f1	260710203604N6H	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
10000	credit	success	T825994295957126	funding	Paystack Funding	0	2026-07-11 13:59:28.268533	d3c4edb1-0c7f-4f7c-aa8b-47af4794c3ea	260711135928KAL	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101240601737	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-11 15:28:52.866386	2fcdf46a-0895-4486-a61e-296b00f337e4	260711152852ZG5	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
20000	credit	success	T323784104260265	funding	Paystack Funding	0	2026-07-11 15:37:58.439519	4852e1ad-f7f3-440e-b56e-9133598aa3dc	260711153758QK5	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201206482	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-11 15:47:34.131673	95df5bff-7895-4cd1-945d-c64efa22ecc8	26071115473492E	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201206482	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-11 15:49:57.564618	84c1f52c-2ce2-4cbe-ad59-cba6a8d73e36	260711154957VWH	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201206482	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-11 16:04:42.545243	2585f7e0-9e6a-4304-82a8-b30d72c44bd3	260711160442BD6	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
20000	credit	success	T758881785829445	funding	Paystack Funding	0	2026-07-12 07:10:40.021873	dee74b2e-7fa6-4ebb-8062-a72f7949bc54	260712071040A4S	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201202386	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-12 12:41:54.72973	7b957ab4-0f47-497e-b0a9-2f8dd2a47f9c	260712124154Z13	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201243157	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-12 13:30:53.24862	8605b0bf-703c-4d87-accc-2aa46cc9b413	26071213305395W	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	REFUND-abbcc603-4cca-4826-ba0f-e7746f1583d6	refund	Refund for failed TV transaction abbcc603-4cca-4826-ba0f-e7746f1583d6	0	2026-07-12 15:11:17.793791	53e98f6e-aa9e-40a7-aa8a-7e9bbb919a05	260712151117JDX	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-AB201204452	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-12 15:10:44.907117	abbcc603-4cca-4826-ba0f-e7746f1583d6	260712151044J9J	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401017882	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-15 11:24:36.540803	21fe0fce-c8df-49a8-9271-e4b1c1f25846	260715112436Z33	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101039273	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-18 16:37:35.22393	87ce6cd6-264d-472f-9291-62fccc454233	260718163735V85	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	failed	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-AB201204452	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-12 15:12:27.201351	6b7b5b34-cd60-40cd-b8e5-5ddfed0b793f	26071215122783X	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	REFUND-6b7b5b34-cd60-40cd-b8e5-5ddfed0b793f	refund	Refund for failed TV transaction 6b7b5b34-cd60-40cd-b8e5-5ddfed0b793f	0	2026-07-12 15:13:05.108367	9aac0dae-01e8-49cc-a54e-17b025ff078a	2607121513050U8	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201052204	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-15 11:17:33.952023	a25d8f04-e832-46a5-a7a8-d8bd0ebe2c43	260715111733R8B	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401008228	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-15 14:51:16.415097	21b60833-cec1-4bc2-b148-40ebf233c971	260715145116F1U	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201204452	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-12 15:14:29.948515	b7a75e38-7b20-479b-ac2b-c6c22dfbae5b	2607121514293CM	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201171031	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-12 17:45:30.659527	30b9ca0d-422d-4857-a543-12146b7e937b	26071217453043A	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
10000	credit	success	T056425322213355	funding	Paystack Funding	0	2026-07-15 11:08:42.436475	d7fbbf94-4e23-40c7-a1c9-acbe95f93b6b	260715110842J8L	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
10000	credit	success	T775732790035165	funding	Paystack Funding	0	2026-07-18 13:23:52.193357	4f1a7848-6722-4b20-8994-32b4444b9d9c	260718132352H3F	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
10000	credit	success	T853253607297224	funding	Paystack Funding	0	2026-07-18 16:36:13.456181	1e1b6a5c-f083-4584-999d-9ae4d69f4b5d	260718163613IRS	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201013150	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-18 13:29:43.983819	41aafe77-66fc-4e41-99ac-94be5184d178	260718132943B4W	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401003035	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-19 08:08:09.787522	fa8c7c31-1d5c-4bfa-8c5f-eaa4ebf2f679	260719080809MLD	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201077747	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-19 08:40:34.61027	7bdb7e70-449d-4912-bac6-059f49447a08	260719084034ZVY	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T138768237267812	funding	Paystack Funding	0	2026-07-19 08:45:39.099397	c05c56ae-74e3-4668-8788-11bc9b504b06	260719084539AKN	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101039273	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-19 08:46:36.206681	39aaf858-fe46-440d-ae4b-53831a8555ef	260719084636QW8	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T829056265274536	funding	Paystack Funding	0	2026-07-19 13:24:56.121845	1cbe9b08-1644-45d6-96c3-535fbcf36a1b	260719132456Y2X	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB301241108655	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-19 13:25:22.276894	4d838c8b-175c-4dc4-a552-b242d83e64de	2607191325222LN	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T636502562621143	funding	Paystack Funding	0	2026-07-19 18:55:44.849222	bd12ff34-73e7-49fd-937e-759ed5d5171f	260719185544879	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB101041091	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-19 18:56:12.333095	e7008916-512b-45d4-a648-ef784444081a	2607191856120T3	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	credit	success	T395747754237540	funding	Paystack Funding	0	2026-07-23 09:42:20.579336	47aec4cf-bfb9-4798-810e-babac9a8c894	26072309422064L	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201019574	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-23 09:42:47.731611	e5b53c7e-cf33-415f-ba92-5df324fdb673	260723094247B5O	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
10000	credit	success	T015577971532704	funding	Paystack Funding	0	2026-07-26 12:02:22.078369	62a9f6e9-ed84-45ca-af9e-c02e31511faa	260726120222UT1	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
10000	credit	success	T107347773284225	funding	Paystack Funding	0	2026-07-26 12:03:51.64032	2dd7dc2c-85f8-459a-bc01-af9fce806ede	260726120351VDS	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
2500	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201110138	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-26 12:06:21.99112	3d64cc80-a2ec-4673-8bd7-9fe480cbef7d	260726120621W2V	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201269017	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-26 12:13:18.843258	71ec7ed5-3dd1-4294-891a-a94bc9d677d2	260726121318J82	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201269017	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-26 12:13:38.675092	7496e54c-8158-43c3-8798-25400bfa6de1	260726121338XL0	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB201269017	tv	Provider: sltv | Local Automation Result: Do not have sufficient balance	0	2026-07-26 12:14:03.093008	0197c894-1e34-457b-a099-c7367e09e697	260726121403306	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
2500	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201110138	tv	Provider: sltv | Local Automation Result: Do not have sufficient balance	0	2026-07-26 12:17:19.251208	0249e4ec-164a-48a5-b1e1-a0d1a0b73b00	260726121719SH6	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
10000	credit	success	T633958835840699	funding	Paystack Funding	0	2026-07-26 17:49:09.775993	bfb949ea-42b1-4ba3-88c0-254591b0f9a3	260726174909NGG	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201290731	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-26 17:52:22.356394	5da1e03e-230e-4fa2-ac4a-5952a32ce826	260726175222CAT	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-0b759c8d-1261-4ca7-889a-2e6745a2ce1e-SB401004007	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-27 08:17:04.712688	64ff5c62-2bfc-42a3-b512-95f560dc7d57	260727081704YTB	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201208184	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-27 17:15:32.024494	d314fd6d-8197-4e5d-bdf0-b61bbcda00b6	260727171532X43	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
6000	credit	success	T348307405214629	funding	Paystack Funding	0	2026-07-27 17:52:01.92635	d8765a88-2581-405c-9c0a-09db598731c0	260727175201GHL	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb101240600328	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-27 17:54:07.413654	b35f6d8c-9a1d-49c5-8df2-c53312923009	2607271754079WQ	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5500	credit	success	T023032039827151	funding	Paystack Funding	0	2026-07-28 19:26:53.537764	423b1e1f-5e4e-42a0-9f0a-3f0850567243	260728192653OVL	fb2c27f9-ceaf-4d78-b271-60f2c2dba78f	efe5e342-c1ad-468a-af42-aaeb36857e77
5000	debit	success	TV-fb2c27f9-ceaf-4d78-b271-60f2c2dba78f-Sb201050033	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-28 19:28:08.326786	1ecc5761-627f-47d9-85b6-0560973a15d7	26072819280899N	fb2c27f9-ceaf-4d78-b271-60f2c2dba78f	efe5e342-c1ad-468a-af42-aaeb36857e77
5000	credit	success	T445841726799320	funding	Paystack Funding	0	2026-07-29 18:16:57.477135	ee41d5e1-9c90-4a0d-8f7b-9393c2864ee6	260729181657S5H	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	failed	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb30110145	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-29 18:20:20.55874	bce42869-3ffe-40d0-899f-e38250c789a3	260729182020X2M	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	REFUND-bce42869-3ffe-40d0-899f-e38250c789a3	refund	Refund for failed TV transaction bce42869-3ffe-40d0-899f-e38250c789a3	0	2026-07-29 18:20:58.481422	2e5c29b8-35b4-40c5-bfbb-75d5402f8607	260729182058PZJ	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	failed	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb30110145	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-07-29 19:00:32.101484	7eeee59f-0934-45e4-a418-e96eee58036d	2607291900327NY	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	REFUND-7eeee59f-0934-45e4-a418-e96eee58036d	refund	Refund for failed TV transaction 7eeee59f-0934-45e4-a418-e96eee58036d	0	2026-07-29 19:01:06.414152	89ce6eee-1503-44f6-baa5-7d2d97e86b6b	260729190106241	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-SB201116304	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-07-29 19:10:58.98132	7c85473b-2e30-45de-9013-ef787965934d	260729191058IEN	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T973970524728193	funding	Paystack Funding	0	2026-08-01 20:56:19.464883	594fae20-5103-4a60-b6e4-bfa39ced9de5	260801205619Z5X	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	success	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SB201006322	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-01 20:57:10.673295	f1786b5f-2b52-422f-8f68-ea620a88c928	260801205710CUX	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	credit	success	T262383154391473	funding	Paystack Funding	0	2026-08-02 15:41:57.344566	43a0c624-e1f1-44cf-8d6b-4698710064ad	2608021541575FX	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	success	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SB201102167	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-03 12:05:22.233771	1e6fddfc-685d-4b4b-ba8f-83208cf66abf	260803120522SIS	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb201226005	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-04 10:39:13.792262	47c17fba-e18a-4c43-8f0b-22e27bc003b0	260804103913T0Q	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb101240600328	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-05 15:03:20.88865	b0c5d439-70dd-4664-834c-dd3dcd0b3d71	260805150320XQO	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb101240600328	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-05 15:03:54.245944	da5bd80d-d1bf-4600-afc5-6d158706303a	260805150354TU2	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SB201205982	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-02 15:43:32.750276	87ebd772-e3bb-4642-8341-ce48842c7b65	260802154332MKZ	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
10000	credit	success	T785463622238061	funding	Paystack Funding	0	2026-08-02 19:29:49.47315	1edd9621-e525-4948-b5a2-36139fc7679b	260802192949STA	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T478799008326085	funding	Paystack Funding	0	2026-08-03 12:02:58.141792	366a0569-fa9d-4b72-a388-af3d64449452	260803120258E35	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb101240600328	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-05 15:02:45.249114	7ab7ba2d-e4d1-4b37-92e0-78ed30ee422d	260805150245R7H	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401010062	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-02 19:30:17.92936	a97f3981-c8d3-4747-89ae-e5a18ae43865	260802193017Z44	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
20000	credit	success	T598346224906646	funding	Paystack Funding	0	2026-08-05 15:02:23.373863	b025521d-e273-4584-8c68-805629d607a3	2608051502235NR	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb101240600328	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-05 15:03:38.681242	7d68dd54-d714-43ab-a39c-a432dd1c35ad	260805150338IJF	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T168912120274822	funding	Paystack Funding	0	2026-08-05 18:46:13.850753	574fef20-608f-4d8a-a6b5-a8554c573c43	260805184613S5I	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401006983	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-05 18:46:36.018026	7a517bb0-6aab-4b19-bc48-1847cea1bc2c	26080518463612I	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
10000	credit	success	T527309095904026	funding	Paystack Funding	0	2026-08-05 19:36:49.528331	edd221d3-f265-4c0c-af67-7d6494a13d85	260805193649UPM	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	failed	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SN-SB201001789	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-08-05 19:40:11.274769	9f0d8d25-9605-4c9d-9a25-82b7e76efaae	260805194011NBA	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	credit	success	REFUND-9f0d8d25-9605-4c9d-9a25-82b7e76efaae	refund	Refund for failed TV transaction 9f0d8d25-9605-4c9d-9a25-82b7e76efaae	0	2026-08-05 19:40:46.592836	036f9b7a-a4d9-450d-b192-aad46ef7f7a7	260805194046RS2	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	failed	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SN-SB201001789	tv	Provider: sltv | Error: Local Automation returned False (failed)	0	2026-08-05 19:40:58.620181	27c5cad9-76bc-419a-a61d-0fa7b687e369	260805194058SUS	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	credit	success	REFUND-27c5cad9-76bc-419a-a61d-0fa7b687e369	refund	Refund for failed TV transaction 27c5cad9-76bc-419a-a61d-0fa7b687e369	0	2026-08-05 19:41:37.688744	ba73d29e-c6b4-47cd-836a-fe81327e1067	260805194137PSR	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	success	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SB101240613502	tv	Provider: sltv | Local Automation Result: Do not have sufficient balance	0	2026-08-05 19:43:55.770041	c5935d34-e1b4-4284-8c47-296113d8dbf2	260805194355HRW	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	success	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SB201001789	tv	Provider: sltv | Local Automation Result: Do not have sufficient balance	0	2026-08-05 19:53:29.266217	6424518c-32f5-47aa-bda7-8b6ecf6a7484	2608051953297GQ	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
10000	credit	success	T934245353336900	funding	Paystack Funding	0	2026-08-09 09:59:26.696024	20f6db7f-80e4-478b-a29a-b7195eb8b542	260809095926H9A	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb401006463	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-09 10:01:45.137122	f4c3ebab-3087-460f-8716-a7799bfcd5b1	260809100145NIU	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb301241101215	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-09 10:10:59.534393	82202cbe-2280-4418-a7b4-7685bc02c8c6	260809101059H0Y	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T398272160471589	funding	Paystack Funding	0	2026-08-09 17:18:29.016968	a375944e-bd5b-461a-8815-065aeb4fd189	260809171829KB1	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	debit	success	TV-a0e237f5-d92f-4f31-bf52-20012874edb1-SB101231005275	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-09 17:19:07.485171	f9242bd2-43dc-4cef-9829-47456dd8fe1d	2608091719074SU	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
5000	credit	success	T417009694552576	funding	Paystack Funding	0	2026-08-12 17:46:22.057374	306b0de7-6002-4885-bdfc-a5646e08f8a1	2608121746221YM	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-SB201202386	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-12 17:51:10.287878	3761d220-28d0-44e0-a19a-d42f0a132087	260812175110K7N	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T594366625794348	funding	Paystack Funding	0	2026-08-13 19:42:58.566368	d3049886-6259-4fe5-b5ef-cc397516ac2f	260813194258GY2	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-308208ff-efc3-4aad-b4aa-3fffd0e4a006-Sb301241105189	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-13 19:43:44.029425	462b8051-e884-4752-89cc-e8dddd7eb71e	2608131943445XF	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T032845494717398	funding	Paystack Funding	0	2026-08-14 12:32:59.698655	2282f96a-ea2f-4e3e-b1ae-dd363efc1828	260814123259S2N	a4b08b75-b1c6-4caa-b409-53b2aac7dfd8	d73374b6-14ac-4ad3-9a76-8d4a36c4315b
1000	debit	failed	AIRTIME-308208ff-efc3-4aad-b4aa-3fffd0e4a006-09155949473	airtime	Network: BAB | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-08-17 11:15:45.301808	0240b40c-c7a2-4aa4-ae73-74adf6b14daa	260817111545ZMO	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	credit	success	REFUND-0240b40c-c7a2-4aa4-ae73-74adf6b14daa	refund	Refund for failed Airtime transaction 0240b40c-c7a2-4aa4-ae73-74adf6b14daa	0	2026-08-17 11:15:45.974269	9b2c44f7-c448-445f-9e6f-4f00fe819a5f	260817111545Q0L	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	debit	failed	AIRTIME-308208ff-efc3-4aad-b4aa-3fffd0e4a006-09155949473	airtime	Network: BAB | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-08-17 11:15:52.062162	fe6a9d94-08e7-46c3-9d35-7d4e1d0ca474	260817111552KR0	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	credit	success	REFUND-fe6a9d94-08e7-46c3-9d35-7d4e1d0ca474	refund	Refund for failed Airtime transaction fe6a9d94-08e7-46c3-9d35-7d4e1d0ca474	0	2026-08-17 11:15:52.514712	1e0e2741-50b2-41e7-9802-a4cead48eead	260817111552ZCO	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	debit	failed	AIRTIME-308208ff-efc3-4aad-b4aa-3fffd0e4a006-09155949473	airtime	Network: BAB | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-08-17 11:15:56.992749	369a080d-54db-41fd-904a-a0b9cf5f7693	260817111556MA3	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	credit	success	REFUND-369a080d-54db-41fd-904a-a0b9cf5f7693	refund	Refund for failed Airtime transaction 369a080d-54db-41fd-904a-a0b9cf5f7693	0	2026-08-17 11:15:57.556989	99191b9a-1f31-4472-a490-a01f1ad0d882	260817111557BE1	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	debit	failed	AIRTIME-308208ff-efc3-4aad-b4aa-3fffd0e4a006-09155949473	airtime	Network: BAB | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-08-17 11:16:02.515034	a92462c2-6ead-4fdd-af3e-38691b7875f4	260817111602VBF	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	credit	success	REFUND-a92462c2-6ead-4fdd-af3e-38691b7875f4	refund	Refund for failed Airtime transaction a92462c2-6ead-4fdd-af3e-38691b7875f4	0	2026-08-17 11:16:02.963657	7f65577f-6fc1-4def-8275-e84ab8718463	260817111602VXZ	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	debit	failed	AIRTIME-308208ff-efc3-4aad-b4aa-3fffd0e4a006-09155949473	airtime	Network: BAB | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-08-17 11:16:03.594647	939f6e30-e0e3-4074-88ed-d1aaf7cea020	260817111603V2P	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
1000	credit	success	REFUND-939f6e30-e0e3-4074-88ed-d1aaf7cea020	refund	Refund for failed Airtime transaction 939f6e30-e0e3-4074-88ed-d1aaf7cea020	0	2026-08-17 11:16:04.024695	43f2523f-9d58-4dcd-ac5e-c1755e05ee6a	260817111604M8C	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
500	debit	failed	AIRTIME-308208ff-efc3-4aad-b4aa-3fffd0e4a006-09155949473	airtime	Network: BAB | Error: You must be a standard user to access this API - kindly upgrade your account	0	2026-08-17 11:17:09.631118	9e6057c6-deb1-4bc9-bfe7-743a2959beb6	2608171117090TY	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	credit	success	T117541964161083	funding	Paystack Funding	0	2026-08-20 19:52:32.339921	82ba01c7-0550-46d9-9142-4d7d1bf72635	260820195232BDF	c9368e77-b726-4d65-b8e8-1a4fb6e16195	89b5793a-59ab-4f04-af43-3b9991f7f82f
500	credit	success	REFUND-9e6057c6-deb1-4bc9-bfe7-743a2959beb6	refund	Refund for failed Airtime transaction 9e6057c6-deb1-4bc9-bfe7-743a2959beb6	0	2026-08-17 11:17:10.047393	696e7297-5ff0-4cda-8308-7f3e4d252fad	260817111710SUS	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
5000	debit	success	TV-a4b08b75-b1c6-4caa-b409-53b2aac7dfd8-SB201278863	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-18 20:31:32.450087	f2dff754-77fe-42fc-a7ae-45800834b947	260818203132P7S	a4b08b75-b1c6-4caa-b409-53b2aac7dfd8	d73374b6-14ac-4ad3-9a76-8d4a36c4315b
5000	debit	success	TV-c9368e77-b726-4d65-b8e8-1a4fb6e16195-SB301241103294	tv	Provider: sltv | Local Automation Result: Smart Card has been recharge successfully	0	2026-08-20 19:54:03.774932	ef717f50-3635-4042-9421-77580fcc84d9	260820195403NFJ	c9368e77-b726-4d65-b8e8-1a4fb6e16195	89b5793a-59ab-4f04-af43-3b9991f7f82f
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."user" (email, is_active, is_superuser, is_verified, full_name, id, hashed_password) FROM stdin;
amiolademilade@gmail.com	t	f	f	Samdavweb	177edb49-8905-4efd-a328-9b0bb8ae64a0	$2b$12$O8a5cyyyW/Ezjlu8oaGoWu74B8u24db62tKtqEEfTBeTUTBNEhLUi
techio.com.ng@gmail.com	t	f	t	Dawodu Samuel	24c60e81-1b39-4e2e-b33d-2c4328a8732b	$2b$12$x6WIywaIDV4gmlathqFzW.PZZFAltX8Jo1NdxlxOAmw6lFEvgdlvC
victorbarnabas24@gmail.com	t	f	f	Victor Odinaka	30af4cd8-e309-44ae-8d6b-0d78e7ce6ee2	$2b$12$i/eOsyIGeP/9LXiP47pZr..iT/aryIz.VT6cE93tlNHArUokcWo6K
ezyshop203@gmail.com	t	f	f	Nwaikwu Izunna Paulinus 	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d	$2b$12$7AiqgY3j/kY5CHCNrNsGNOhLX/ZJF220ARXvB5kCSmwGN.BUfD4u6
bloggers694@gmail.com	t	f	t	Samuel Dawodu X	04585b5e-2f46-4d39-bf1c-025b510f577c	$2b$12$rlqLwUNJFqPzpV7N6cqe9.XQBkZQRG/nvgmUkLo/eSDV3KaYOl7ES
ikedimmajc@gmail.com	t	f	f	Ikedimma Johnbosco Chijioke 	efe5e342-c1ad-468a-af42-aaeb36857e77	$2b$12$I/k7u35K5W2T5vvn3Cfq1OkJldcrBetsIgwkA2DqZxZ.TNgWqOPy.
nnabusomething@gmail.com	t	f	f	Okonkwo Nnabuife Ugochukwu 	130457d5-a2fd-4ab8-aebf-055f67a0881e	$2b$12$QWt2AbTJ6hNhjDyO8F3agOjczAhPaQQ/O9vVuLs6iXhRoqigADUBy
christonwana@gmail.com	t	f	f	Nwana Obiora 	89b5793a-59ab-4f04-af43-3b9991f7f82f	$2b$12$yWwpkIDtpCpzaxsPbQbYyeyWRBfXtoP8mPZMpkLLlgFZ885fcEIvW
okoroaforjulius@gmail.com	t	f	f	Okoroafor Julius	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0	$2b$12$WiBo6dPBpnSoi7bNjxidK.XR12q9lmmtWX7y/BJKMxizB8z/tL7hu
ezeanyamathias15@gmail.com	t	f	f	Ezeanya Chinweokwu 	1a19d029-08e4-4f5c-a67f-6e6bbc5ea9bc	$2b$12$5DExTmhVFS0vDRdlWneiwOed7A3LMQ7ry4Q8VSnjgv91F5/SPmhU6
ifeanyi0006@gmail.com	t	f	f	AJALA ifeanyi Emmanuel 	c191f95a-0595-47e7-ab63-3601101424e2	$2b$12$Jnw8IFkDcR6pqHxBxvO10eRCcG9wKpi/.9d4MF4r6V68T.T7nwjFC
victorifey58@gmail.com	t	f	t	Ifedilichukwu Emmanuel 	478140a8-2ea5-43a1-bc88-6b170cd62eac	$2b$12$gZ2a7xeMwWspWn4khB.2IOvJO62gbaH/3mJjie7LOfc7v7XsXcevy
lollyyyyyyy30@gmail.com	t	f	t	dami lola	d7cef85b-6f87-45ff-9580-9c4f6a247a5d	$2b$12$yuKCtq1OAK.GkN8uvNhIGeYoEKcO9KSJfSruzlQ.KkszFFqW11a/6
princeokoro14@gmail.com	t	f	t	SDD SOLAR COMPANY 	f0ba467e-f24c-46fe-87a4-2e8d27946b80	$2b$12$BelqRcIN8V2eW66k2951LuLLnAu1WOMzO1E5uxsNWFn9M/1JO0dQu
nwufohchicason25@gmail.com	t	f	t	Nwufoh Frederick chika	da26c950-9583-4183-b846-1a74d4d86329	$2b$12$7r3VWVveK2p6vKdcyBmaze.Y4w.2341x.QOYcmaGIi8zQdcn/ozly
nanchip183@gmail.com	t	f	f	Amala Idris	066e4cb1-73fb-40f3-869e-39857819b557	$2b$12$AVlQJ.leReoqTGfo/Mcgauuk53iACDMQmr67z1KZ4GHPpOY6rzvI6
anthonychinenyeesther@gmail.com	t	f	f	Nwufoh Chinenye 	2221b6a6-c5a2-40e3-af65-25bcebb9daa0	$2b$12$gYo5fgYB2fYIFoxZPvUve.I.1ySzHgT2l48svV4jyrEX.6aDO3OL2
Stephenanyaka44@gmail.com	t	f	f	Anyaka Stephen ifeanyi 	d73374b6-14ac-4ad3-9a76-8d4a36c4315b	$2b$12$mqk94LdOL.QElf.d6fZtm.ATpoQg5hzhUUJA9qlWmm.oYbyUY3kKi
suleimanmustapha053@gmail.com	t	f	f	Suleiman mustapha 	6aa45ad3-aed1-4407-b57f-0714c83d564b	$2b$12$2RgHH7SOUf0hQC1IFpwJcuHqH9bQpSxUzEabtw3fkWw0J74wN8hWm
\.


--
-- Data for Name: user_profile; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.user_profile (full_name, phone_number, address, state, lga, nin, bvn, id, user_id) FROM stdin;
Samuel Iyanu Dawodu	07064205836	60, jamiuraji Street	Lagos				1ae60961-1b18-4490-897a-89ca0604ed0c	04585b5e-2f46-4d39-bf1c-025b510f577c
Nwufoh Chicason	08068907784	No 14 Arthur Eze Ave.	Anambra	Awka South 			d625cac5-2e7a-4a8f-bb91-943ba93b95d3	da26c950-9583-4183-b846-1a74d4d86329
Okoro Etinosa. David	07012129090	No 1okoro street off limit road benin city 	Edo	Oredeo	30085167899	22180289967	ba88d417-17e2-4256-bdfd-ab80eca7606f	f0ba467e-f24c-46fe-87a4-2e8d27946b80
\.


--
-- Data for Name: wallet; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.wallet (balance, currency, id, user_id) FROM stdin;
0	NGN	ee46e7ae-b7d0-429e-a1df-23079e6a5309	177edb49-8905-4efd-a328-9b0bb8ae64a0
0	NGN	63418c94-2140-4030-94e6-9aa48fa3effe	24c60e81-1b39-4e2e-b33d-2c4328a8732b
0	NGN	92ae507f-1d98-46cb-baa9-839c865edb78	30af4cd8-e309-44ae-8d6b-0d78e7ce6ee2
0	NGN	0a3ffbba-74e4-40b4-981f-ee94ddc8b22f	04585b5e-2f46-4d39-bf1c-025b510f577c
0	NGN	d6690f92-b426-4465-8d56-90768d5d981c	c4c26141-ec5a-4a6c-bf12-ab4e8e3c7af0
0	NGN	13ae3f4d-ba71-49c3-a6da-018cfb28b832	d7cef85b-6f87-45ff-9580-9c4f6a247a5d
0	NGN	26de5ccb-ad77-4ce8-9cd5-59ded920f7da	66fb30a3-1f2d-4876-bd2f-86ee4c9db78d
0	NGN	a12f2e29-1db5-4790-b778-7a59718da0aa	1a19d029-08e4-4f5c-a67f-6e6bbc5ea9bc
0	NGN	2c1662ff-e025-4f30-9d21-b9b5efc16ff7	2221b6a6-c5a2-40e3-af65-25bcebb9daa0
0	NGN	a0e237f5-d92f-4f31-bf52-20012874edb1	130457d5-a2fd-4ab8-aebf-055f67a0881e
0	NGN	4904f770-76cc-41d4-af2b-d5e796d5925a	478140a8-2ea5-43a1-bc88-6b170cd62eac
0	NGN	156093ea-c7f8-4e3e-bf8f-5a856a31b4cf	6aa45ad3-aed1-4407-b57f-0714c83d564b
200	NGN	30ae425f-efe5-410d-a495-7ff9094c6b02	f0ba467e-f24c-46fe-87a4-2e8d27946b80
0	NGN	0b759c8d-1261-4ca7-889a-2e6745a2ce1e	da26c950-9583-4183-b846-1a74d4d86329
0	NGN	bb099af9-e7ed-44e7-adbb-da8c666ab199	066e4cb1-73fb-40f3-869e-39857819b557
1000	NGN	308208ff-efc3-4aad-b4aa-3fffd0e4a006	c191f95a-0595-47e7-ab63-3601101424e2
500	NGN	fb2c27f9-ceaf-4d78-b271-60f2c2dba78f	efe5e342-c1ad-468a-af42-aaeb36857e77
0	NGN	a4b08b75-b1c6-4caa-b409-53b2aac7dfd8	d73374b6-14ac-4ad3-9a76-8d4a36c4315b
0	NGN	c9368e77-b726-4d65-b8e8-1a4fb6e16195	89b5793a-59ab-4f04-af43-3b9991f7f82f
\.


--
-- Name: admin admin_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.admin
    ADD CONSTRAINT admin_pkey PRIMARY KEY (id);


--
-- Name: service_price service_price_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.service_price
    ADD CONSTRAINT service_price_pkey PRIMARY KEY (id);


--
-- Name: ticket_message ticket_message_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ticket_message
    ADD CONSTRAINT ticket_message_pkey PRIMARY KEY (id);


--
-- Name: ticket ticket_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_pkey PRIMARY KEY (id);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_profile user_profile_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.user_profile
    ADD CONSTRAINT user_profile_pkey PRIMARY KEY (id);


--
-- Name: user_profile user_profile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.user_profile
    ADD CONSTRAINT user_profile_user_id_key UNIQUE (user_id);


--
-- Name: wallet wallet_pkey; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.wallet
    ADD CONSTRAINT wallet_pkey PRIMARY KEY (id);


--
-- Name: wallet wallet_user_id_key; Type: CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.wallet
    ADD CONSTRAINT wallet_user_id_key UNIQUE (user_id);


--
-- Name: ix_admin_email; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_admin_email ON public.admin USING btree (email);


--
-- Name: ix_service_price_service_identifier; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_service_price_service_identifier ON public.service_price USING btree (service_identifier);


--
-- Name: ix_transaction_trans_id; Type: INDEX; Schema: public; Owner: admin
--

CREATE INDEX ix_transaction_trans_id ON public.transaction USING btree (trans_id);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: admin
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ticket_message ticket_message_admin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ticket_message
    ADD CONSTRAINT ticket_message_admin_id_fkey FOREIGN KEY (admin_id) REFERENCES public.admin(id);


--
-- Name: ticket_message ticket_message_sender_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ticket_message
    ADD CONSTRAINT ticket_message_sender_id_fkey FOREIGN KEY (sender_id) REFERENCES public."user"(id);


--
-- Name: ticket_message ticket_message_ticket_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ticket_message
    ADD CONSTRAINT ticket_message_ticket_id_fkey FOREIGN KEY (ticket_id) REFERENCES public.ticket(id);


--
-- Name: ticket ticket_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.ticket
    ADD CONSTRAINT ticket_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: transaction transaction_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: transaction transaction_wallet_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.transaction
    ADD CONSTRAINT transaction_wallet_id_fkey FOREIGN KEY (wallet_id) REFERENCES public.wallet(id);


--
-- Name: user_profile user_profile_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.user_profile
    ADD CONSTRAINT user_profile_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: wallet wallet_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.wallet
    ADD CONSTRAINT wallet_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 6ZCvtbLS7kBCeXI6EvT67CiP34iSolYO02EmTQiODwoL85xaAuL2WPsAxBjY5BB

