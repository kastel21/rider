SET NOCOUNT ON;
BEGIN TRANSACTION;

IF OBJECT_ID(N'dbo.auth_group', N'U') IS NOT NULL DROP TABLE dbo.auth_group;
CREATE TABLE dbo.[auth_group] (
  [id] INT NOT NULL,
  [name] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_auth_group] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.auth_group_permissions', N'U') IS NOT NULL DROP TABLE dbo.auth_group_permissions;
CREATE TABLE dbo.[auth_group_permissions] (
  [id] INT NOT NULL,
  [group_id] INT NOT NULL,
  [permission_id] INT NOT NULL,
  CONSTRAINT [PK_auth_group_permissions] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.auth_permission', N'U') IS NOT NULL DROP TABLE dbo.auth_permission;
CREATE TABLE dbo.[auth_permission] (
  [id] INT NOT NULL,
  [content_type_id] INT NOT NULL,
  [codename] NVARCHAR(MAX) NOT NULL,
  [name] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_auth_permission] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.auth_user', N'U') IS NOT NULL DROP TABLE dbo.auth_user;
CREATE TABLE dbo.[auth_user] (
  [id] INT NOT NULL,
  [password] NVARCHAR(MAX) NOT NULL,
  [last_login] NVARCHAR(MAX) NULL,
  [is_superuser] NVARCHAR(MAX) NOT NULL,
  [username] NVARCHAR(MAX) NOT NULL,
  [last_name] NVARCHAR(MAX) NOT NULL,
  [email] NVARCHAR(MAX) NOT NULL,
  [is_staff] NVARCHAR(MAX) NOT NULL,
  [is_active] NVARCHAR(MAX) NOT NULL,
  [date_joined] NVARCHAR(MAX) NOT NULL,
  [first_name] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_auth_user] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.auth_user_groups', N'U') IS NOT NULL DROP TABLE dbo.auth_user_groups;
CREATE TABLE dbo.[auth_user_groups] (
  [id] INT NOT NULL,
  [user_id] INT NOT NULL,
  [group_id] INT NOT NULL,
  CONSTRAINT [PK_auth_user_groups] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.auth_user_user_permissions', N'U') IS NOT NULL DROP TABLE dbo.auth_user_user_permissions;
CREATE TABLE dbo.[auth_user_user_permissions] (
  [id] INT NOT NULL,
  [user_id] INT NOT NULL,
  [permission_id] INT NOT NULL,
  CONSTRAINT [PK_auth_user_user_permissions] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.django_admin_log', N'U') IS NOT NULL DROP TABLE dbo.django_admin_log;
CREATE TABLE dbo.[django_admin_log] (
  [id] INT NOT NULL,
  [object_id] NVARCHAR(MAX) NULL,
  [object_repr] NVARCHAR(MAX) NOT NULL,
  [action_flag] NVARCHAR(MAX) NOT NULL,
  [change_message] NVARCHAR(MAX) NOT NULL,
  [content_type_id] INT NULL,
  [user_id] INT NOT NULL,
  [action_time] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_django_admin_log] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.django_content_type', N'U') IS NOT NULL DROP TABLE dbo.django_content_type;
CREATE TABLE dbo.[django_content_type] (
  [id] INT NOT NULL,
  [app_label] NVARCHAR(MAX) NOT NULL,
  [model] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_django_content_type] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.django_session', N'U') IS NOT NULL DROP TABLE dbo.django_session;
CREATE TABLE dbo.[django_session] (
  [session_key] NVARCHAR(MAX) NOT NULL,
  [session_data] NVARCHAR(MAX) NOT NULL,
  [expire_date] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_django_session] PRIMARY KEY ([session_key])
);

IF OBJECT_ID(N'dbo.operations_bike', N'U') IS NOT NULL DROP TABLE dbo.operations_bike;
CREATE TABLE dbo.[operations_bike] (
  [id] INT NOT NULL,
  [code] NVARCHAR(MAX) NOT NULL,
  [notes] NVARCHAR(MAX) NOT NULL,
  [active] NVARCHAR(MAX) NOT NULL,
  [district_id] NVARCHAR(MAX) NULL,
  [snp_bike_accident] INT NOT NULL,
  [snp_bike_breakdown] INT NOT NULL,
  [snp_bike_no_fuel] INT NOT NULL,
  [snp_bike_routine_service] INT NOT NULL,
  [snp_clinical_ip] INT NOT NULL,
  [snp_inclement_weather] INT NOT NULL,
  [snp_other] INT NOT NULL,
  [snp_other_specify] NVARCHAR(MAX) NOT NULL,
  [snp_rider_annual_leave] INT NOT NULL,
  [snp_rider_sick_leave] INT NOT NULL,
  [mitigation_measures] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_bike] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_bike_affected_facilities', N'U') IS NOT NULL DROP TABLE dbo.operations_bike_affected_facilities;
CREATE TABLE dbo.[operations_bike_affected_facilities] (
  [id] INT NOT NULL,
  [bike_id] NVARCHAR(MAX) NOT NULL,
  [facility_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_bike_affected_facilities] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_car', N'U') IS NOT NULL DROP TABLE dbo.operations_car;
CREATE TABLE dbo.[operations_car] (
  [id] INT NOT NULL,
  [code] NVARCHAR(MAX) NOT NULL,
  [notes] NVARCHAR(MAX) NOT NULL,
  [active] NVARCHAR(MAX) NOT NULL,
  [snp_bike_breakdown] INT NOT NULL,
  [snp_bike_routine_service] INT NOT NULL,
  [snp_bike_no_fuel] INT NOT NULL,
  [snp_rider_sick_leave] INT NOT NULL,
  [snp_rider_annual_leave] INT NOT NULL,
  [snp_inclement_weather] INT NOT NULL,
  [snp_bike_accident] INT NOT NULL,
  [snp_clinical_ip] INT NOT NULL,
  [snp_other] INT NOT NULL,
  [snp_other_specify] NVARCHAR(MAX) NOT NULL,
  [mitigation_measures] NVARCHAR(MAX) NOT NULL,
  [district_id] NVARCHAR(MAX) NULL,
  CONSTRAINT [PK_operations_car] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_car_affected_facilities', N'U') IS NOT NULL DROP TABLE dbo.operations_car_affected_facilities;
CREATE TABLE dbo.[operations_car_affected_facilities] (
  [id] INT NOT NULL,
  [car_id] NVARCHAR(MAX) NOT NULL,
  [facility_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_car_affected_facilities] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_district', N'U') IS NOT NULL DROP TABLE dbo.operations_district;
CREATE TABLE dbo.[operations_district] (
  [id] INT NOT NULL,
  [name] NVARCHAR(MAX) NOT NULL,
  [province_id] NVARCHAR(MAX) NOT NULL,
  [support_type] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_district] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_facility', N'U') IS NOT NULL DROP TABLE dbo.operations_facility;
CREATE TABLE dbo.[operations_facility] (
  [id] INT NOT NULL,
  [name] NVARCHAR(MAX) NOT NULL,
  [kind] NVARCHAR(MAX) NOT NULL,
  [district_id] NVARCHAR(MAX) NOT NULL,
  [support_type] NVARCHAR(MAX) NOT NULL,
  [site_code] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_facility] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_lab', N'U') IS NOT NULL DROP TABLE dbo.operations_lab;
CREATE TABLE dbo.[operations_lab] (
  [id] INT NOT NULL,
  [name] NVARCHAR(MAX) NOT NULL,
  [code] NVARCHAR(MAX) NOT NULL,
  [updated_at] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_lab] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_pcdistrictweeklytransportstat', N'U') IS NOT NULL DROP TABLE dbo.operations_pcdistrictweeklytransportstat;
CREATE TABLE dbo.[operations_pcdistrictweeklytransportstat] (
  [id] INT NOT NULL,
  [week_start] NVARCHAR(MAX) NOT NULL,
  [rider_accidents] INT NOT NULL,
  [incomplete_bike_transport_trips] INT NOT NULL,
  [specimens_non_ist_total] INT NOT NULL,
  [specimens_ambulance] INT NOT NULL,
  [specimens_alternative_ip_transport] INT NOT NULL,
  [specimens_mohcc_arranged_transport] INT NOT NULL,
  [specimens_courier] INT NOT NULL,
  [specimens_other_non_ist] INT NOT NULL,
  [comments] NVARCHAR(MAX) NOT NULL,
  [created_at] NVARCHAR(MAX) NOT NULL,
  [updated_at] NVARCHAR(MAX) NOT NULL,
  [district_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_pcdistrictweeklytransportstat] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_pcprofile', N'U') IS NOT NULL DROP TABLE dbo.operations_pcprofile;
CREATE TABLE dbo.[operations_pcprofile] (
  [id] INT NOT NULL,
  [user_id] INT NOT NULL,
  CONSTRAINT [PK_operations_pcprofile] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_pcprofile_provinces', N'U') IS NOT NULL DROP TABLE dbo.operations_pcprofile_provinces;
CREATE TABLE dbo.[operations_pcprofile_provinces] (
  [id] INT NOT NULL,
  [pcprofile_id] NVARCHAR(MAX) NOT NULL,
  [province_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_pcprofile_provinces] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_province', N'U') IS NOT NULL DROP TABLE dbo.operations_province;
CREATE TABLE dbo.[operations_province] (
  [id] INT NOT NULL,
  [name] NVARCHAR(MAX) NOT NULL,
  [code] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_province] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_referredsample', N'U') IS NOT NULL DROP TABLE dbo.operations_referredsample;
CREATE TABLE dbo.[operations_referredsample] (
  [id] INT NOT NULL,
  [sample_type] NVARCHAR(MAX) NOT NULL,
  [test_type] NVARCHAR(MAX) NOT NULL,
  [total_samples_referred_out] INT NOT NULL,
  [swift_consignment_number] NVARCHAR(MAX) NOT NULL,
  [comments] NVARCHAR(MAX) NOT NULL,
  [created_at] NVARCHAR(MAX) NOT NULL,
  [from_facility_id] NVARCHAR(MAX) NOT NULL,
  [to_facility_id] NVARCHAR(MAX) NULL,
  CONSTRAINT [PK_operations_referredsample] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_registereddevice', N'U') IS NOT NULL DROP TABLE dbo.operations_registereddevice;
CREATE TABLE dbo.[operations_registereddevice] (
  [id] INT NOT NULL,
  [device_id] NVARCHAR(MAX) NOT NULL,
  [platform] NVARCHAR(MAX) NOT NULL,
  [user_agent] NVARCHAR(MAX) NOT NULL,
  [last_seen_at] NVARCHAR(MAX) NOT NULL,
  [created_at] NVARCHAR(MAX) NOT NULL,
  [user_id] INT NOT NULL,
  CONSTRAINT [PK_operations_registereddevice] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_reportauditlog', N'U') IS NOT NULL DROP TABLE dbo.operations_reportauditlog;
CREATE TABLE dbo.[operations_reportauditlog] (
  [id] INT NOT NULL,
  [action] NVARCHAR(MAX) NOT NULL,
  [payload] NVARCHAR(MAX) NOT NULL,
  [created_at] NVARCHAR(MAX) NOT NULL,
  [actor_id] INT NULL,
  [report_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_reportauditlog] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_reporteditsnapshot', N'U') IS NOT NULL DROP TABLE dbo.operations_reporteditsnapshot;
CREATE TABLE dbo.[operations_reporteditsnapshot] (
  [id] INT NOT NULL,
  [summary] NVARCHAR(MAX) NOT NULL,
  [diff_data] NVARCHAR(MAX) NOT NULL,
  [created_at] NVARCHAR(MAX) NOT NULL,
  [editor_id] INT NULL,
  [report_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_reporteditsnapshot] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_riderdevice', N'U') IS NOT NULL DROP TABLE dbo.operations_riderdevice;
CREATE TABLE dbo.[operations_riderdevice] (
  [id] INT NOT NULL,
  [device_id] NVARCHAR(MAX) NOT NULL,
  [device_model] NVARCHAR(MAX) NOT NULL,
  [app_version] NVARCHAR(MAX) NOT NULL,
  [last_seen] NVARCHAR(MAX) NOT NULL,
  [is_active] NVARCHAR(MAX) NOT NULL,
  [rider_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_riderdevice] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_riderprofile', N'U') IS NOT NULL DROP TABLE dbo.operations_riderprofile;
CREATE TABLE dbo.[operations_riderprofile] (
  [id] INT NOT NULL,
  [bike_id] NVARCHAR(MAX) NULL,
  [district_id] NVARCHAR(MAX) NULL,
  [facility_id] NVARCHAR(MAX) NULL,
  [user_id] INT NOT NULL,
  [province_id] NVARCHAR(MAX) NULL,
  [support_type] NVARCHAR(MAX) NOT NULL,
  [car_id] NVARCHAR(MAX) NULL,
  CONSTRAINT [PK_operations_riderprofile] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_riderremoteconfig', N'U') IS NOT NULL DROP TABLE dbo.operations_riderremoteconfig;
CREATE TABLE dbo.[operations_riderremoteconfig] (
  [id] INT NOT NULL,
  [sync_interval] INT NOT NULL,
  [max_batch_size] INT NOT NULL,
  [latest_app_version] NVARCHAR(MAX) NOT NULL,
  [update_required] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_riderremoteconfig] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_ridertripentry', N'U') IS NOT NULL DROP TABLE dbo.operations_ridertripentry;
CREATE TABLE dbo.[operations_ridertripentry] (
  [id] INT NOT NULL,
  [row_uuid] NVARCHAR(MAX) NOT NULL,
  [sequence] INT NOT NULL,
  [entry_date] NVARCHAR(MAX) NULL,
  [vl_blood_plasma] INT NOT NULL,
  [vl_dbs] INT NOT NULL,
  [eid_blood] INT NOT NULL,
  [eid_dbs] INT NOT NULL,
  [sputum] INT NOT NULL,
  [sputum_culture_dr] INT NOT NULL,
  [hpv] INT NOT NULL,
  [specimens_other_specify] NVARCHAR(MAX) NOT NULL,
  [results_vl_blood_plasma] INT NOT NULL,
  [results_vl_dbs] INT NOT NULL,
  [results_eid_blood] INT NOT NULL,
  [results_eid_dbs] INT NOT NULL,
  [results_sputum] INT NOT NULL,
  [results_sputum_culture_dr] INT NOT NULL,
  [results_hpv] INT NOT NULL,
  [results_other_specify] NVARCHAR(MAX) NOT NULL,
  [fuel_allocated] NVARCHAR(MAX) NOT NULL,
  [fuel_used] NVARCHAR(MAX) NOT NULL,
  [distance_travelled] NVARCHAR(MAX) NOT NULL,
  [created_at] NVARCHAR(MAX) NOT NULL,
  [updated_at] NVARCHAR(MAX) NOT NULL,
  [report_id] NVARCHAR(MAX) NOT NULL,
  [destination_facility_id] NVARCHAR(MAX) NULL,
  [origin_facility_id] NVARCHAR(MAX) NULL,
  [route_kind] NVARCHAR(MAX) NOT NULL,
  [visit_purpose] NVARCHAR(MAX) NOT NULL,
  [transport_kind] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_ridertripentry] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_riderweeklyreport', N'U') IS NOT NULL DROP TABLE dbo.operations_riderweeklyreport;
CREATE TABLE dbo.[operations_riderweeklyreport] (
  [id] INT NOT NULL,
  [client_uuid] NVARCHAR(MAX) NULL,
  [week_start] NVARCHAR(MAX) NOT NULL,
  [status] NVARCHAR(MAX) NOT NULL,
  [title] NVARCHAR(MAX) NOT NULL,
  [notes] NVARCHAR(MAX) NOT NULL,
  [samples_collected] INT NOT NULL,
  [extra_data] NVARCHAR(MAX) NOT NULL,
  [submitted_at] NVARCHAR(MAX) NULL,
  [review_started_at] NVARCHAR(MAX) NULL,
  [reviewed_at] NVARCHAR(MAX) NULL,
  [pc_notes] NVARCHAR(MAX) NOT NULL,
  [created_at] NVARCHAR(MAX) NOT NULL,
  [updated_at] NVARCHAR(MAX) NOT NULL,
  [reviewed_by_id] INT NULL,
  [rider_id] INT NOT NULL,
  [bike_id] NVARCHAR(MAX) NULL,
  [scheduled_visits] INT NULL,
  [average_datalogger_temperature] INT NULL,
  [car_id] NVARCHAR(MAX) NULL,
  CONSTRAINT [PK_operations_riderweeklyreport] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_samplerejection', N'U') IS NOT NULL DROP TABLE dbo.operations_samplerejection;
CREATE TABLE dbo.[operations_samplerejection] (
  [id] INT NOT NULL,
  [sample_type] NVARCHAR(MAX) NOT NULL,
  [rejected_total] INT NOT NULL,
  [rejected_too_old] INT NOT NULL,
  [rejected_patient_info_mismatch] INT NOT NULL,
  [rejected_request_form_missing] INT NOT NULL,
  [rejected_sample_missing] INT NOT NULL,
  [rejected_other] INT NOT NULL,
  [order] NVARCHAR(MAX) NOT NULL,
  [report_id] NVARCHAR(MAX) NOT NULL,
  CONSTRAINT [PK_operations_samplerejection] PRIMARY KEY ([id])
);

IF OBJECT_ID(N'dbo.operations_userprofile', N'U') IS NOT NULL DROP TABLE dbo.operations_userprofile;
CREATE TABLE dbo.[operations_userprofile] (
  [id] INT NOT NULL,
  [role] NVARCHAR(MAX) NOT NULL,
  [user_id] INT NOT NULL,
  CONSTRAINT [PK_operations_userprofile] PRIMARY KEY ([id])
);

-- auth_permission
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (1, 1, N'add_logentry', N'Can add log entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (2, 1, N'change_logentry', N'Can change log entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (3, 1, N'delete_logentry', N'Can delete log entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (4, 1, N'view_logentry', N'Can view log entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (5, 2, N'add_permission', N'Can add permission');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (6, 2, N'change_permission', N'Can change permission');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (7, 2, N'delete_permission', N'Can delete permission');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (8, 2, N'view_permission', N'Can view permission');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (9, 3, N'add_group', N'Can add group');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (10, 3, N'change_group', N'Can change group');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (11, 3, N'delete_group', N'Can delete group');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (12, 3, N'view_group', N'Can view group');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (13, 4, N'add_user', N'Can add user');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (14, 4, N'change_user', N'Can change user');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (15, 4, N'delete_user', N'Can delete user');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (16, 4, N'view_user', N'Can view user');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (17, 5, N'add_contenttype', N'Can add content type');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (18, 5, N'change_contenttype', N'Can change content type');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (19, 5, N'delete_contenttype', N'Can delete content type');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (20, 5, N'view_contenttype', N'Can view content type');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (21, 6, N'add_session', N'Can add session');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (22, 6, N'change_session', N'Can change session');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (23, 6, N'delete_session', N'Can delete session');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (24, 6, N'view_session', N'Can view session');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (25, 7, N'add_bike', N'Can add bike');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (26, 7, N'change_bike', N'Can change bike');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (27, 7, N'delete_bike', N'Can delete bike');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (28, 7, N'view_bike', N'Can view bike');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (29, 8, N'add_district', N'Can add district');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (30, 8, N'change_district', N'Can change district');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (31, 8, N'delete_district', N'Can delete district');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (32, 8, N'view_district', N'Can view district');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (33, 9, N'add_province', N'Can add province');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (34, 9, N'change_province', N'Can change province');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (35, 9, N'delete_province', N'Can delete province');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (36, 9, N'view_province', N'Can view province');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (37, 10, N'add_facility', N'Can add facility');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (38, 10, N'change_facility', N'Can change facility');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (39, 10, N'delete_facility', N'Can delete facility');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (40, 10, N'view_facility', N'Can view facility');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (41, 11, N'add_pcprofile', N'Can add pc profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (42, 11, N'change_pcprofile', N'Can change pc profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (43, 11, N'delete_pcprofile', N'Can delete pc profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (44, 11, N'view_pcprofile', N'Can view pc profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (45, 12, N'add_riderprofile', N'Can add rider profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (46, 12, N'change_riderprofile', N'Can change rider profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (47, 12, N'delete_riderprofile', N'Can delete rider profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (48, 12, N'view_riderprofile', N'Can view rider profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (49, 13, N'add_riderweeklyreport', N'Can add rider weekly report');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (50, 13, N'change_riderweeklyreport', N'Can change rider weekly report');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (51, 13, N'delete_riderweeklyreport', N'Can delete rider weekly report');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (52, 13, N'view_riderweeklyreport', N'Can view rider weekly report');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (53, 14, N'add_reporteditsnapshot', N'Can add report edit snapshot');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (54, 14, N'change_reporteditsnapshot', N'Can change report edit snapshot');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (55, 14, N'delete_reporteditsnapshot', N'Can delete report edit snapshot');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (56, 14, N'view_reporteditsnapshot', N'Can view report edit snapshot');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (57, 15, N'add_reportauditlog', N'Can add report audit log');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (58, 15, N'change_reportauditlog', N'Can change report audit log');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (59, 15, N'delete_reportauditlog', N'Can delete report audit log');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (60, 15, N'view_reportauditlog', N'Can view report audit log');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (61, 16, N'add_userprofile', N'Can add user profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (62, 16, N'change_userprofile', N'Can change user profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (63, 16, N'delete_userprofile', N'Can delete user profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (64, 16, N'view_userprofile', N'Can view user profile');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (65, 17, N'add_registereddevice', N'Can add registered device');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (66, 17, N'change_registereddevice', N'Can change registered device');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (67, 17, N'delete_registereddevice', N'Can delete registered device');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (68, 17, N'view_registereddevice', N'Can view registered device');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (69, 18, N'add_ridertripentry', N'Can add rider trip entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (70, 18, N'change_ridertripentry', N'Can change rider trip entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (71, 18, N'delete_ridertripentry', N'Can delete rider trip entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (72, 18, N'view_ridertripentry', N'Can view rider trip entry');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (73, 19, N'add_samplerejection', N'Can add Sample rejection');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (74, 19, N'change_samplerejection', N'Can change Sample rejection');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (75, 19, N'delete_samplerejection', N'Can delete Sample rejection');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (76, 19, N'view_samplerejection', N'Can view Sample rejection');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (77, 20, N'add_car', N'Can add car');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (78, 20, N'change_car', N'Can change car');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (79, 20, N'delete_car', N'Can delete car');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (80, 20, N'view_car', N'Can view car');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (81, 21, N'add_referredsample', N'Can add referred sample');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (82, 21, N'change_referredsample', N'Can change referred sample');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (83, 21, N'delete_referredsample', N'Can delete referred sample');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (84, 21, N'view_referredsample', N'Can view referred sample');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (85, 22, N'add_pcdistrictweeklytransportstat', N'Can add pc district weekly transport stat');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (86, 22, N'change_pcdistrictweeklytransportstat', N'Can change pc district weekly transport stat');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (87, 22, N'delete_pcdistrictweeklytransportstat', N'Can delete pc district weekly transport stat');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (88, 22, N'view_pcdistrictweeklytransportstat', N'Can view pc district weekly transport stat');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (89, 23, N'add_lab', N'Can add lab');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (90, 23, N'change_lab', N'Can change lab');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (91, 23, N'delete_lab', N'Can delete lab');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (92, 23, N'view_lab', N'Can view lab');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (93, 24, N'add_riderremoteconfig', N'Can add Rider Remote Config');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (94, 24, N'change_riderremoteconfig', N'Can change Rider Remote Config');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (95, 24, N'delete_riderremoteconfig', N'Can delete Rider Remote Config');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (96, 24, N'view_riderremoteconfig', N'Can view Rider Remote Config');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (97, 25, N'add_riderdevice', N'Can add rider device');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (98, 25, N'change_riderdevice', N'Can change rider device');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (99, 25, N'delete_riderdevice', N'Can delete rider device');
INSERT INTO dbo.[auth_permission] ([id], [content_type_id], [codename], [name]) VALUES (100, 25, N'view_riderdevice', N'Can view rider device');

-- auth_user
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (1, N'pbkdf2_sha256$1200000$oEqstqS9vUmVLjH1sq8iS9$qaH6SPexHTXNhEfvpo4HSXQUaYAjdMqfFaJtS17Yg44=', N'2026-04-08 07:03:35.388561', 1, N'admin', N'', N't@k.com', 1, 1, N'2026-04-08 06:54:14.256038', N'');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (2, N'pbkdf2_sha256$1000000$1tgyD1D243W8xd7WoJYn5i$OlnitL/16xrn8ESTra0w6FV94j6VSHuzUXCLtMM0BIU=', NULL, 0, N'blessed_mudhumo', N'', N'', 0, 1, N'2026-04-08 07:04:59.470676', N'Blessed Mudhumo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (3, N'pbkdf2_sha256$1200000$zEe9qxS5pY17aVYrrMFOrZ$ZXFXIif9cpWCKstYkCY5dez8W1AR/oHQdlVe/NEXlpQ=', N'2026-04-08 17:44:00.058337', 0, N'clemence_gatsi', N'', N'', 0, 1, N'2026-04-08 07:05:00.147965', N'Clemence Gatsi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (4, N'pbkdf2_sha256$1000000$9tikknRSE7uzxP4wZM5rJi$j/l0ZToDx9sDmotkLqvgWaY/HLAdt56NytXmUQ+Iv08=', NULL, 0, N'edmore_mukaronda', N'', N'', 0, 1, N'2026-04-08 07:05:00.875365', N'Edmore Mukaronda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (5, N'pbkdf2_sha256$1000000$vgi8MxjRKgyhLyq5T8F3bo$ENuwvzh4cckqi8+3bkCe9QkSo0V8SIMAnPqJP5bCZPg=', NULL, 0, N'faustina_tasara', N'', N'', 0, 1, N'2026-04-08 07:05:01.474632', N'Faustina Tasara');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (6, N'pbkdf2_sha256$1000000$6LuyWsU5GS0i2WClpgb04w$6SIGysw5AZviwzjXeJ6xUdijzstNHyQGaJPBy4NPRC8=', NULL, 0, N'lisben_maguwu', N'', N'', 0, 1, N'2026-04-08 07:05:02.157875', N'Lisben Maguwu');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (7, N'pbkdf2_sha256$1000000$IX5dEIzX9MfGQaFKKoeb7w$TA+RR6U9oV5Ifq1glqKmxtEOD5Y/hC/Z/zjgMGj5ySQ=', NULL, 0, N'mavis_moyo', N'', N'', 0, 1, N'2026-04-08 07:05:02.728808', N'Mavis Moyo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (8, N'pbkdf2_sha256$1000000$49BdAb3Vz3VTMQLYzzM48D$sy6lF5UQj7G/kyRyiKancH1FCFnZFMhhE9ybjlo6f5g=', NULL, 0, N'nyasha_tsvangirai', N'', N'', 0, 1, N'2026-04-08 07:05:03.248624', N'Nyasha Tsvangirai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (9, N'pbkdf2_sha256$1000000$QJZN9kICFQ2LWevbQrJnx5$9OwvnvQSDwRWbxuSuFndYcJvHJgmSk/25tT/zV8ywMU=', NULL, 0, N'philiph_muzavazi', N'', N'', 0, 1, N'2026-04-08 07:05:03.770702', N'Philiph Muzavazi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (10, N'pbkdf2_sha256$1000000$U7HNrJcKEpIcJqSussOT3C$6RQbmBp+1d7AAvq0UohT7nCN0J/SdAQOGfwVQjh4RTE=', N'2026-04-08 13:33:51.035910', 0, N'promise_mhlanga', N'Mhlanga', N'', 0, 1, N'2026-04-08 09:05:11.623257', N'Promise');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (11, N'pbkdf2_sha256$1000000$gG0TomRSHUtitoLyTiscmG$2mgeAbLo3U6Iot/vO/pZ51lm0nNJ+hAuVsCW7HqCclo=', NULL, 0, N'jonathan_madanhi', N'Madanhi', N'', 0, 1, N'2026-04-08 09:05:12.158977', N'Jonathan');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (12, N'pbkdf2_sha256$1000000$C73zH8r527jhAFyJx6I30L$ARmLXgAhLwILjee9xEmqyd68ohYtDaAU4VhrwtvFjs0=', NULL, 0, N'abel_nyoni', N'Nyoni', N'', 0, 1, N'2026-04-08 09:05:12.691251', N'Abel');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (13, N'pbkdf2_sha256$1000000$x0Krb2NtCKhUsnq2U4aORY$CW/cZC5H/DAcin/AEp8PMGe0B1CnX/7XDFLq/WsN8Lo=', NULL, 0, N'stancilous_rice', N'Rice', N'', 0, 1, N'2026-04-08 09:05:13.243790', N'Stancilous');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (14, N'pbkdf2_sha256$1000000$fa63XOO7VPmZwJG2YcUOVh$GhlKO+Jg2J0GE2Dtr/uUSeUV4fghQHWH4f9yeEhkOU4=', NULL, 0, N'godfrey_magwizi', N'Magwizi', N'', 0, 1, N'2026-04-08 09:05:13.882885', N'Godfrey');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (15, N'pbkdf2_sha256$1000000$v7360A4Q2FkH0wopNuVHMA$ITnOJDjtjis0F2k7bharN6FvOV48eRBT0Ry7QSv5IYs=', NULL, 0, N'archibald_dandara', N'Dandara', N'', 0, 1, N'2026-04-08 09:05:14.957491', N'Archibald');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (16, N'pbkdf2_sha256$1000000$blRDZ4bRalcgZ43Nqao3k8$RQWuFDgmk9trdnK2nFEJMpM5owuV7IAHWcx+fQjZRuk=', NULL, 0, N'wilford_nyanzero', N'Nyanzero', N'', 0, 1, N'2026-04-08 09:05:15.849671', N'Wilford');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (17, N'pbkdf2_sha256$1000000$OlPmDwbEUmpi7KYvPJoUUa$Qa3Vj+cxcMyG1114Vab4BV/r0allOZUJw9j2tjXw83s=', NULL, 0, N'tawanda_gumi', N'Gumi', N'', 0, 1, N'2026-04-08 09:05:16.888018', N'Tawanda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (18, N'pbkdf2_sha256$1000000$BWTQPbSrkU2WgheLcYnJ5d$QkbrqzOVbZVtCmFW6Imaf81ALhsixGaQwPFpnEPnl2Q=', NULL, 0, N'shelton_muriravanhu', N'Muriravanhu', N'', 0, 1, N'2026-04-08 09:05:17.773456', N'Shelton');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (19, N'pbkdf2_sha256$1000000$HRAOdz9va1UM31i9txFz95$uAsmSEyUJjpM8OA3o/ahUlDwMaa4VU7VKLT8l1RoIjs=', NULL, 0, N'bothwell_maorera', N'Maorera', N'', 0, 1, N'2026-04-08 09:05:18.726932', N'Bothwell');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (20, N'pbkdf2_sha256$1000000$fyZBGUHwEANMgLEsNFERme$inTNgCteMf95gblEX/cvjNz807DYa0MpEJfH+y7IoGw=', NULL, 0, N'jaison_tarovedzera', N'Tarovedzera', N'', 0, 1, N'2026-04-08 09:05:19.591278', N'Jaison');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (21, N'pbkdf2_sha256$1000000$Iqsb7TpDZdRyYALwWDjpds$D6njodIxs12dRqQWBZ5QIy9DL0PkCZQiZM+uBfePUhM=', NULL, 0, N'bigboy_manzunzu', N'manzunzu', N'', 0, 1, N'2026-04-08 09:05:20.571240', N'Bigboy');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (22, N'pbkdf2_sha256$1000000$TFwpAKJ6fPVvZTt2IYXVd3$Vc1JJfXTIRl88u2e+/6G3OxJijIEJY3+QlPYlJqNR60=', NULL, 0, N'egton_tsuronzuma', N'Tsuronzuma', N'', 0, 1, N'2026-04-08 09:05:21.575250', N'Egton');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (23, N'pbkdf2_sha256$1000000$vU1DtIh1G1o1FybX57udto$xSx8wNK/NAmWv/kSE0VeIOv0jTyzuC3AnlaSE0NFyMs=', NULL, 0, N'matengarufu_blessing', N'Blessing', N'', 0, 1, N'2026-04-08 09:05:22.756196', N'Matengarufu');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (24, N'pbkdf2_sha256$1000000$oV3dKwR3cKIW9o1SZXcXOq$srA51pVmlBO8N3SME3G5wwMVmne5xpzz1Drk+BzC5bY=', NULL, 0, N'sabao_pineas', N'Pineas', N'', 0, 1, N'2026-04-08 09:05:24.271906', N'sabao');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (25, N'pbkdf2_sha256$1000000$1SMsmbHV0gVyVAHj4CWxkg$nNC3nYvGUA77pV2RfW2DOvMQMGyVMdq+Xd/E8quulXg=', NULL, 0, N'mugwambi_taurai', N'Taurai', N'', 0, 1, N'2026-04-08 09:05:25.363643', N'Mugwambi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (26, N'pbkdf2_sha256$1000000$EHMVHjD8gGQ2YoPaq5bRGz$n2RSQGu6w8ajELUIDdUHwO+Tvti5ijVnqnPINY5zSZ4=', NULL, 0, N'chabata_walter', N'Walter', N'', 0, 1, N'2026-04-08 09:05:26.445180', N'Chabata');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (27, N'pbkdf2_sha256$1000000$O1PG7WtxXnC6h5T8sYVQ0f$OlQWCuys93rHCMKV3cav8+4zBAZP1deGwjAbOsm6PLc=', NULL, 0, N'edward_maworere', N'Maworere', N'', 0, 1, N'2026-04-08 09:05:27.748962', N'Edward');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (28, N'pbkdf2_sha256$1000000$IMdpYj8apeqZA5jcvjoLSH$KKs5EvdoKbWFIVw3vPm/QWI00vWvTLFEvMFlMv/xJcM=', NULL, 0, N'blessing_bindura', N'bindura', N'', 0, 1, N'2026-04-08 09:05:28.951339', N'Blessing');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (29, N'pbkdf2_sha256$1000000$41eOURKkdrTM5cengoCv4F$Dfr9cxpE4YtNDRE8WKz0vQZEn3TYzzzbkog5v5fJJuw=', NULL, 0, N'elias_mutombera', N'Mutombera', N'', 0, 1, N'2026-04-08 09:05:30.489642', N'Elias');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (30, N'pbkdf2_sha256$1000000$wWL2acOObPdWggNlVEySz8$Q4RjudYi7o8po8RIbTVWl+hRYwMj6TyE8R3pwe6mHVo=', NULL, 0, N'norest_madzingowenyu', N'Madzingowenyu', N'', 0, 1, N'2026-04-08 09:05:31.896974', N'Norest');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (31, N'pbkdf2_sha256$1000000$0k17OdcjmCngrhpAco3wND$Yp9DuO8d3+TDAwmOGYyfQN+o5+7zJ7q1qxQN6sv1E68=', NULL, 0, N'ngwira_george', N'George', N'', 0, 1, N'2026-04-08 09:05:32.759634', N'Ngwira');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (32, N'pbkdf2_sha256$1000000$yEJQCWu0UiANYUeFPUN0SF$a77x5uOuxC6vqq5WGXJS+RSpHueOJwTnuEBgutRMCyI=', NULL, 0, N'myambo_giyani', N'Giyani', N'', 0, 1, N'2026-04-08 09:05:33.846506', N'Myambo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (33, N'pbkdf2_sha256$1000000$UlxwrRnpMW364iVOOeHJCN$X1xH6XIx3ntiuGnaFzdCS626UK1F46S6uPoGXd4HFAk=', NULL, 0, N'bornmore_sithole', N'Sithole', N'', 0, 1, N'2026-04-08 09:05:35.014387', N'Bornmore');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (34, N'pbkdf2_sha256$1000000$fbpLWieOWvHQNHqZHvhvWF$9joCu4AkpAd6nIEXkJ2Z7dHOVBS3lgVBbNofz9cnok0=', NULL, 0, N'chikukwa_peter', N'Peter', N'', 0, 1, N'2026-04-08 09:05:35.934390', N'Chikukwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (35, N'pbkdf2_sha256$1000000$RO4pfofrHhyHrM5nvp3ztZ$ir+BgCaDoW0eAeofY4WFWVdC8h3iJ5uFVlYyXrVXAPc=', NULL, 0, N'pedzsai_mupsambangoma', N'Mupsambangoma', N'', 0, 1, N'2026-04-08 09:05:36.802345', N'Pedzsai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (36, N'pbkdf2_sha256$1000000$VwUrLAqPF3xFtwcfuwfV9l$POuHru2c0avX/5mR56l57b5/auwyvVwapmL5ZwdplnI=', NULL, 0, N'musariarwa_liberty', N'Liberty', N'', 0, 1, N'2026-04-08 09:05:37.648839', N'Musariarwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (37, N'pbkdf2_sha256$1000000$ylA8yrpric8rbthTgrqhgk$lCsKKXXayk7NUPDyZRQNXDM33tAXPvC0XSyxQCCJxZ8=', NULL, 0, N'chigona_richmore', N'Richmore', N'', 0, 1, N'2026-04-08 09:05:38.630445', N'Chigona');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (38, N'pbkdf2_sha256$1000000$IYDcJemnRV88nOIX4Zukqv$u7DNEKMeeAiWkIKYkdzXFGxS7ueCIa8GkkjrK55HaWI=', NULL, 0, N'ndhlovu_lawrence', N'Lawrence', N'', 0, 1, N'2026-04-08 09:05:39.637549', N'Ndhlovu');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (39, N'pbkdf2_sha256$1000000$5vuavqkX8wGzJn4fh0NCQ5$7XEW+wWkBaXfA68lpsAUFcGbc+2yPQDoIpf7i02d3hg=', NULL, 0, N'gwati_kaurisayi', N'Kaurisayi', N'', 0, 1, N'2026-04-08 09:05:40.493456', N'Gwati');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (40, N'pbkdf2_sha256$1000000$ji0fO46zUs3qopDGdgzcLr$fn/e0ChuovoZiUwg88C3DvEQnoPHTn5/iy264LaYTAA=', NULL, 0, N'mafudza_farai', N'Farai', N'', 0, 1, N'2026-04-08 09:05:41.408439', N'Mafudza');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (41, N'pbkdf2_sha256$1000000$8CXQA3PX5ZMheIwUe7cwus$uzN3i9WNmx7iF8DUIZDIRAw/NhqJX0Ya7jL4INa9YqQ=', NULL, 0, N'bepe_jackson', N'Jackson', N'', 0, 1, N'2026-04-08 09:05:42.412937', N'Bepe');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (42, N'pbkdf2_sha256$1000000$kJHYxyStIvil1uPzQb8tPS$kFFezfItkWAaSRvv6NBwLRI5s3ppeO+w8PgKWr8d+RU=', NULL, 0, N'nyangani_simba', N'Simba', N'', 0, 1, N'2026-04-08 09:05:43.365533', N'Nyangani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (43, N'pbkdf2_sha256$1000000$7fQXNuV6EOG1kvxlUHZStJ$B41cBkJkVfH0suw9V9RgUNXe3ZdRDJCHgKxLPvmsR4s=', NULL, 0, N'bhobhojani_brighton', N'Brighton', N'', 0, 1, N'2026-04-08 09:05:44.342309', N'Bhobhojani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (44, N'pbkdf2_sha256$1000000$dSq3UB5eLvco1zm25MpwiX$N5MiZG2Xf6mG0DrCJ1FGJgxUdv5rcD+2bEe37YPoWrg=', NULL, 0, N'aron_chawanda', N'Chawanda', N'', 0, 1, N'2026-04-08 09:05:45.420854', N'Aron');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (45, N'pbkdf2_sha256$1000000$Bot0g2CsMmzmFB7XqMW7tv$D64E6zjK+INFX+87KMAz6iDmLhFP0Emqn4drmBTDxFg=', NULL, 0, N'namanga_prince', N'Prince', N'', 0, 1, N'2026-04-08 09:05:46.377168', N'Namanga');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (46, N'pbkdf2_sha256$1000000$YAWKPiIBlOuxlPEqOEOD1O$nyJVVlJg06CY6ERh+ssyK9zIRQYebscrqKAzGAD2ctU=', NULL, 0, N'ruhukwa_gladmore', N'Gladmore', N'', 0, 1, N'2026-04-08 09:05:47.233054', N'Ruhukwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (47, N'pbkdf2_sha256$1000000$KgxbDlM9gfNOoMEzlZJK8h$oE9yuzXCD91vH39QnmuRzmoRJkgGGZRHOoxurxZOZvM=', NULL, 0, N'masimbe_george', N'George', N'', 0, 1, N'2026-04-08 09:05:48.216478', N'Masimbe');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (48, N'pbkdf2_sha256$1000000$HIjscfYOjOdY917WMxhBnh$tS387nKKRP4NkHRptHjA3VnwzTSaI2rnAUFse1DekAA=', NULL, 0, N'kumbefu_clement', N'Clement', N'', 0, 1, N'2026-04-08 09:05:49.205698', N'Kumbefu');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (49, N'pbkdf2_sha256$1000000$6ds4X6sSPU0aDUOHAPwdLw$+bYlU0IM7YRdTrfhjh2BDDVxNCHJ37GgH9WqWn7ZnMI=', NULL, 0, N'hajapi_prosper', N'Prosper', N'', 0, 1, N'2026-04-08 09:05:49.971453', N'Hajapi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (50, N'pbkdf2_sha256$1000000$Wy1PkwjlnkBExsvBkWcuoT$VItcrYdIFC118BEhlx9N9YHG2cGX2/Q/CJgoGOrB5AM=', NULL, 0, N'chigwanda_carryforward', N'Carryforward', N'', 0, 1, N'2026-04-08 09:05:50.703623', N'Chigwanda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (51, N'pbkdf2_sha256$1000000$DdEL3VcY35L1dh5rV9gUkG$p8NE3dm5U9Hqn+pysLhhqeKRPNhAdsGT/CqtHhFq37Q=', NULL, 0, N'mukorera_tatenda', N'Tatenda', N'', 0, 1, N'2026-04-08 09:05:51.531397', N'Mukorera');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (52, N'pbkdf2_sha256$1000000$3bTeJk7Nikr147gyLq432C$dX8FUeQmu3w9YP9uDDaFVEQMbfDkTVzdOtZjmPd03gg=', NULL, 0, N'mutara_bekithemba', N'Bekithemba', N'', 0, 1, N'2026-04-08 09:05:52.398234', N'Mutara');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (53, N'pbkdf2_sha256$1000000$dou0koYbcgsEBDmJFd4iLU$tmkBO9LPRbaMbc7MX/M2T9txb18/ia7654yrotsUQ0w=', NULL, 0, N'nyakatawa_david', N'David', N'', 0, 1, N'2026-04-08 09:05:53.281945', N'Nyakatawa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (54, N'pbkdf2_sha256$1000000$pwJdZJ7PTEHQO5cw9nPeMX$PL9kNmPkhVJAwCIW6IjgRkipljh8Ml7Dq18bRuAE5zw=', NULL, 0, N'tengwi_john', N'John', N'', 0, 1, N'2026-04-08 09:05:54.117666', N'Tengwi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (55, N'pbkdf2_sha256$1000000$ZtJpLmnVsS85RnemvlenBN$BrQR/ADBnbWAMBg9gZpg+PYLaaNy/3R6Orz5gy4GatY=', NULL, 0, N'godknows_dube', N'Dube', N'', 0, 1, N'2026-04-08 09:05:54.989380', N'Godknows');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (56, N'pbkdf2_sha256$1000000$JFccrj9QyWMcueu3Qmh1xn$gck/JASTQ1YaE2+bz629gU8CpzNv/404nnHm8QVmjks=', NULL, 0, N'lloyd_sande', N'Sande', N'', 0, 1, N'2026-04-08 09:05:55.781644', N'Lloyd');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (57, N'pbkdf2_sha256$1000000$JkuXzfdrvf8jXZ0aUKpP4j$/Sgi1I6rZJkVVO4CyKxD5bp24jQDc50nsW25VVwmslA=', NULL, 0, N'talaent_mutongomanya', N'Mutongomanya', N'', 0, 1, N'2026-04-08 09:05:56.501915', N'Talaent');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (58, N'pbkdf2_sha256$1000000$kx2SQZJHQwSL7yupXV764C$X+/htuQ0Y2UKasC4OE/CjJjaDuJxZAfUXyBheMVR+BQ=', NULL, 0, N'david_sango', N'Sango', N'', 0, 1, N'2026-04-08 09:05:57.358623', N'David');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (59, N'pbkdf2_sha256$1000000$qT98xJM1e1DdHaq94ajX40$Le9/sOABifWqXadjVQYg+jtzy1/9rYYJ2VDDBkpEpVs=', NULL, 0, N'grand_kapumha', N'Kapumha', N'', 0, 1, N'2026-04-08 09:05:58.526243', N'Grand');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (60, N'pbkdf2_sha256$1000000$WKql30GkFu5QyCyUkwA2DG$F1H6ctAQDU9HjQKs5dZjPfIHWKT1a3PHVtjdDNhm0yI=', NULL, 0, N'bruce_randinyo', N'Randinyo', N'', 0, 1, N'2026-04-08 09:05:59.515155', N'Bruce');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (61, N'pbkdf2_sha256$1000000$6fBeMr2qNdvQ3eT5UsTQhi$4YGowYicheMh7udNQlcAf2Rvv2f//crlzVu9Z/EbeWo=', NULL, 0, N'freeman_mutepfe', N'Mutepfe', N'', 0, 1, N'2026-04-08 09:06:00.374424', N'Freeman');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (62, N'pbkdf2_sha256$1000000$hrKhepYxveXIxoIAAIvTg9$k5VQC9ndkTcyASDpyMQnInCv3TbgeYhQo8yJW3w4MrM=', NULL, 0, N'ezekiel_masikati', N'Masikati', N'', 0, 1, N'2026-04-08 09:06:01.166372', N'Ezekiel');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (63, N'pbkdf2_sha256$1000000$QqUyLd7WFy0G0B7SKPE1df$UK/KqlRvleDmWulp9OJ2z/SVAPLb2NjTSO4xMR+4l+s=', NULL, 0, N'wallace_mutasa', N'Mutasa', N'', 0, 1, N'2026-04-08 09:06:02.034886', N'Wallace');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (64, N'pbkdf2_sha256$1000000$7uqykNXfqsFMPSu6ptZzkO$IxsJ/rK8HiC+ekDA2F6WQuic1QsEmhppaXX1sHFU1gI=', NULL, 0, N'simende_give_more', N'Give more', N'', 0, 1, N'2026-04-08 09:06:02.933956', N'simende');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (65, N'pbkdf2_sha256$1000000$jQXZOrhrxnsi5SYMGHDRE8$UIHOWtvUcK5cSMd6a1vaVr3IaGRZYv2m9HTumvdrBgI=', NULL, 0, N'maxwell_munyoro', N'Munyoro', N'', 0, 1, N'2026-04-08 09:06:03.828130', N'Maxwell');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (66, N'pbkdf2_sha256$1000000$AQ1eAOO8ihPy0HKm7YzcLK$OeAgSX9kec3ZFjuzSdsI9F3LoCdyyBjqkn6huo4IMYs=', NULL, 0, N'levie_matengenzara', N'Matengenzara', N'', 0, 1, N'2026-04-08 09:06:04.620987', N'Levie');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (67, N'pbkdf2_sha256$1000000$7Z8MDz4LDuXOojKZ0UyISQ$BeYIqiVjzuivyKDhdIVT94j8LbvP/pEvorzGccUc1BY=', NULL, 0, N'steven_mashumba', N'Mashumba', N'', 0, 1, N'2026-04-08 09:06:05.693141', N'Steven');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (68, N'pbkdf2_sha256$1000000$MW3e65K0zTsJiyuvW9PwUm$dyBKdPJrk9VfAu1GJ1WK8fZxIvOxVpBzWNB6e30RAAg=', NULL, 0, N'abiyoma_chaora', N'Chaora', N'', 0, 1, N'2026-04-08 09:06:06.739298', N'Abiyoma');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (69, N'pbkdf2_sha256$1000000$Qwt2gfyNmtKzDN9oYN2jW6$obMH01rmL6YAo/dBIL4BZPMXMx6fILaqig3WZX2HeAw=', NULL, 0, N'paul_gomo', N'Gomo', N'', 0, 1, N'2026-04-08 09:06:07.790197', N'Paul');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (70, N'pbkdf2_sha256$1000000$djpQ3OVKBu08c1Zv77sBFc$lBXzepXHjqssPuxQ3VHeBZfNS07VzZoe2w54Xi40UJs=', NULL, 0, N'wilson_mupetura', N'Mupetura', N'', 0, 1, N'2026-04-08 09:06:08.820440', N'Wilson');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (71, N'pbkdf2_sha256$1000000$DQZBnDr8qCIwT6je6mmHuP$eGMvW4uMcsn0o9ohSJyvUZeJqUBEqCHVT5ylVjw518s=', NULL, 0, N'blessed_nyoni', N'Nyoni', N'', 0, 1, N'2026-04-08 09:06:09.890150', N'Blessed');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (72, N'pbkdf2_sha256$1000000$mDx50QKQ5P9lFfToa5fBiR$eI4EgWDe7B7zkRnEEnZ+aW0JLDjCKP7gbswhKxNmu/4=', NULL, 0, N'tinotenda_tahuwona', N'Tahuwona', N'', 0, 1, N'2026-04-08 09:06:10.866265', N'Tinotenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (73, N'pbkdf2_sha256$1000000$mBlRBqrBjMvZMEMbngDlOm$pgv/9G7/V7VClICNvSpmFBxAdeBaadO/rn1TurGGrHc=', NULL, 0, N'endure_sigauke', N'Sigauke', N'', 0, 1, N'2026-04-08 09:06:11.549272', N'Endure');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (74, N'pbkdf2_sha256$1000000$QpWAFX6HWRKJ8qYb9cRzIS$YufpKK4tuUxu4yclcmkJdOHA8lgcXvwj/OoYVft/vpA=', NULL, 0, N'tatenda_shamhu', N'Shamhu', N'', 0, 1, N'2026-04-08 09:06:12.100989', N'Tatenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (75, N'pbkdf2_sha256$1000000$aFwmUr6J2MPoJqwhNA3Wkc$n5F1NM+i3wcIZv6ydKJS37KMmYEeevTv8PZbTLlDamw=', NULL, 0, N'joseph_magodo', N'Magodo', N'', 0, 1, N'2026-04-08 09:06:13.081066', N'Joseph');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (76, N'pbkdf2_sha256$1000000$osEmLCMPrVDvEfXrVWpbhh$yL6bDDGYJdy16B1rRkU1R1s2ixR8y91m0Gio8ARN+qo=', NULL, 0, N'thabani_moyo', N'Moyo', N'', 0, 1, N'2026-04-08 09:06:14.325737', N'Thabani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (77, N'pbkdf2_sha256$1000000$XrGScIXOTyAvaRsmDHZubV$DIsfWQ6KATh8mv2hob9q5+PsDWpfY6k71WmQnCOl1xo=', NULL, 0, N'rodney_mafirakureva', N'Mafirakureva', N'', 0, 1, N'2026-04-08 09:06:15.323531', N'Rodney');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (78, N'pbkdf2_sha256$1000000$g8MVJg4PvsvKhCVU4gfwWn$Bl9VVua8UnHTep9znzjNfo36s7ci0UCSrJMFVpxmRjE=', NULL, 0, N'kadere_john', N'John', N'', 0, 1, N'2026-04-08 09:06:16.230091', N'Kadere');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (79, N'pbkdf2_sha256$1000000$Xbxr4ptWvaZ1GYARkLK5Na$XcA8YG6hrc8/JV7XATQNzEbg/UaMq4fMSMwUVIDAhQg=', NULL, 0, N'syria_chamunorwa', N'Chamunorwa', N'', 0, 1, N'2026-04-08 09:06:17.101645', N'Syria');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (80, N'pbkdf2_sha256$1000000$y7c01eSYexUFwfKVPqsfSh$yI1xLXxoaOI2bqIx3Lh+hYD1He/Rvlr9R33z9fVD3ZI=', NULL, 0, N'ashburner_sango', N'Sango', N'', 0, 1, N'2026-04-08 09:06:17.992165', N'Ashburner');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (81, N'pbkdf2_sha256$1000000$Pic1sCRIxRu6rfX0zUKxMX$cscoa24tcPL272NGZLCvDo68Zp5czUK8/QZTmzHMQ3w=', NULL, 0, N'hunzvi_farai', N'Farai', N'', 0, 1, N'2026-04-08 09:06:18.743436', N'Hunzvi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (82, N'pbkdf2_sha256$1000000$9UpGjtOWO1Z50R6rHyMl4f$rDrgc9RLLeBiI3vmlpAT8fLkmLL0/yVl+mGTemiwYa8=', NULL, 0, N'munenyasha_chakanyuka', N'Chakanyuka', N'', 0, 1, N'2026-04-08 09:06:19.479563', N'Munenyasha');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (83, N'pbkdf2_sha256$1000000$AGHPiwV172RYZx502uzLad$vyWvl8UyX+Hk/eKQMA36gucAS216pKc2uVrzMCzaltU=', NULL, 0, N'gift_tapiwa_chiurawa', N'Tapiwa Chiurawa', N'', 0, 1, N'2026-04-08 09:06:20.240133', N'Gift');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (84, N'pbkdf2_sha256$1000000$oe6XNI9IGLEiI6WrzTcg5A$Z2voFTvIEC9qRK76YPohkoROEjhhad7Cx/DowNKskN0=', NULL, 0, N'vincent_madimutsa', N'Madimutsa', N'', 0, 1, N'2026-04-08 09:06:20.988597', N'Vincent');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (85, N'pbkdf2_sha256$1000000$CkXzUqonEpDyVUxYrQ4od4$dbg/+KDX/43ONkdWV4ynUpmBogP6RkskkghcH1yzfqM=', NULL, 0, N'munyoro_brian', N'Brian', N'', 0, 1, N'2026-04-08 09:06:21.789644', N'Munyoro');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (86, N'pbkdf2_sha256$1000000$IUtcVCkuXvUCCqUAhuJkDz$CXYBTvCiwntD6wJbI3EH2BckLZx7l2hifsHoLnoqgoY=', NULL, 0, N'collen_matimura', N'Matimura', N'', 0, 1, N'2026-04-08 09:06:22.736657', N'Collen');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (87, N'pbkdf2_sha256$1000000$ChRAMY10pqqjoFijprqGKm$Dsmol5tFWJ9+n14ELYhbfG3/3iR/B7bV+otFb1HnWxI=', NULL, 0, N'munyaradzi_zvobwo', N'Zvobwo', N'', 0, 1, N'2026-04-08 09:06:23.729664', N'Munyaradzi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (88, N'pbkdf2_sha256$1000000$4Arst0C9rEGV9xR8VdXIZN$xui4JGkAQpAMiMKSTrd+steai6LtlsH5JAGfIZ4Dp6s=', NULL, 0, N'knowledge_makuni', N'Makuni', N'', 0, 1, N'2026-04-08 09:06:24.731747', N'Knowledge');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (89, N'pbkdf2_sha256$1000000$AY8l4RSkAUVoHFBZiCs9F5$p8yzuTeNwMS6zG0S96HH+/FgRKc6V5D2Lew/Mf0GPJo=', NULL, 0, N'hillary_phiri', N'Phiri', N'', 0, 1, N'2026-04-08 09:06:25.565471', N'Hillary');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (90, N'pbkdf2_sha256$1000000$Xs9nX6atFZdKSvOz2ZIGVR$GC+Wo4MmJLkqu7zL6NWRYLmouHmTAYu0/YMWsbyfOUI=', NULL, 0, N'silence_marumahoko', N'Marumahoko', N'', 0, 1, N'2026-04-08 09:06:26.473015', N'Silence');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (91, N'pbkdf2_sha256$1000000$WkfZSMXUAfSjM2wBGNSdsq$bap8xA7WTxg9sPoXWPaFnmSHsa9mQ9kDYhhPR99GS3M=', NULL, 0, N'luckyman_nyandoro', N'Nyandoro', N'', 0, 1, N'2026-04-08 09:06:27.312485', N'Luckyman');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (92, N'pbkdf2_sha256$1000000$RQkKzJ7ag1FnJFRfJLlqas$pl8W1qGDuNS3ySBmZvFZnC+F1SsBUfjTtYLLM++6vR4=', NULL, 0, N'raikosi_chipendo', N'Chipendo', N'', 0, 1, N'2026-04-08 09:06:28.212159', N'Raikosi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (93, N'pbkdf2_sha256$1000000$ljYEXklV2JHMVd0q3PG8ZJ$MBPWZvc9NDF/Hy/Jwo/UuziOY3NVo0w9jNICREuVM0c=', NULL, 0, N'mwenga_ian', N'Ian', N'', 0, 1, N'2026-04-08 09:06:29.052597', N'Mwenga');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (94, N'pbkdf2_sha256$1000000$0tzWalXxiVdv3UFCbYbLuv$SB1lFmFQf/xoWzL7qRrNjEvybUu5TfLH9Za0xuGB7fY=', NULL, 0, N'clever_majoka', N'Majoka', N'', 0, 1, N'2026-04-08 09:06:30.043817', N'Clever');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (95, N'pbkdf2_sha256$1000000$0j9qjpnPUX4VhXMM6L5ToB$SVhXn5ZCG7eVfGPHT5V3HFCRe13JmB5ZA8yArHwjulQ=', NULL, 0, N'kristabell_mashamba', N'Mashamba', N'', 0, 1, N'2026-04-08 09:06:30.961225', N'Kristabell');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (96, N'pbkdf2_sha256$1000000$fKXZUVPZTlYMMkzAzqiuok$aWXcTfEZB3Vj3Mf1J+yO1y8mR5eA3eiOHa30l+OQJ6E=', NULL, 0, N'wellington_t_zimunda', N'T Zimunda', N'', 0, 1, N'2026-04-08 09:06:31.849066', N'Wellington');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (97, N'pbkdf2_sha256$1000000$qTDNrGX68vvVwD2qM1tKrp$PKSHRlLiFjjUQst37sjr4hQ2CseGIaQhEaoNI2Q4obI=', NULL, 0, N'blessing_mahoko', N'Mahoko', N'', 0, 1, N'2026-04-08 09:06:32.835621', N'Blessing');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (98, N'pbkdf2_sha256$1000000$om9JGtDNo5SDugGHBVf42B$rLLOw2sUcmw/b+WW871iS/YcnfyeNCsFBs+i10awyBs=', NULL, 0, N'kudakwashe_severa', N'Severa', N'', 0, 1, N'2026-04-08 09:06:33.843219', N'Kudakwashe');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (99, N'pbkdf2_sha256$1000000$lqg8iL5X7mNh7uT96NaReQ$BVHGPXeuG33v0KRnj4/N+LQLT7ipnkO36r/P7ALn1Cg=', NULL, 0, N'moses_chiwara', N'Chiwara', N'', 0, 1, N'2026-04-08 09:06:34.716152', N'Moses');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (100, N'pbkdf2_sha256$1000000$X4sERcnAx9rcSNdf2yxYG0$7Q9qaZFoSZnDzjp0kBYX512lNXjU08LdZV00e0UhAFU=', NULL, 0, N'cloupus_zifamba', N'Zifamba', N'', 0, 1, N'2026-04-08 09:06:35.213793', N'Cloupus');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (101, N'pbkdf2_sha256$1000000$cWj71NU9AWuQHEj4DoTI0d$mDzI1Pwc9NlDWyH29iguhU9T7x/BCo84xKD3OLWnVXg=', NULL, 0, N'talent_nyamutenha', N'Nyamutenha', N'', 0, 1, N'2026-04-08 09:06:35.671829', N'Talent');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (102, N'pbkdf2_sha256$1000000$VvLd0xGP3rc27r6OsKGv9P$WZfNyNdUVR4ozKhQY9gtY3zGNQ15tZcYVy5eRcSHAHw=', NULL, 0, N'macdonald_mukombe', N'Mukombe', N'', 0, 1, N'2026-04-08 09:06:36.099252', N'MacDonald');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (103, N'pbkdf2_sha256$1000000$X2U25PhblrrvadOuVad2CE$ouOgIbCL8KxXimVY3wFMIu5Zs6W6pyVn0XUN29Qt4oQ=', NULL, 0, N'kelvin_mangoma', N'Mangoma', N'', 0, 1, N'2026-04-08 09:06:36.516343', N'Kelvin');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (104, N'pbkdf2_sha256$1000000$s9qWHj3EasvzuIgWg9uKST$wkt89AAJzwX4sSJKuaTDbVRUUSVD5D1nP2bh3hos+wo=', NULL, 0, N'gibson_chikwizo', N'Chikwizo', N'', 0, 1, N'2026-04-08 09:06:37.031462', N'Gibson');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (105, N'pbkdf2_sha256$1000000$5tqpUARbJkgECQhx7V4qLV$nv/sjql+3tS/nJrS7W4JPI8mmTeJwZysSffqNtY03e8=', NULL, 0, N'adam_chipembere', N'Chipembere', N'', 0, 1, N'2026-04-08 09:06:37.446865', N'Adam');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (106, N'pbkdf2_sha256$1000000$2176A8SE4jenQsCoR1btGR$8aVuRfoWRkF4nsvKHaONTqQrwL7JJFPhZw5srncFcFM=', NULL, 0, N'zvichapera_kabaya', N'Kabaya', N'', 0, 1, N'2026-04-08 09:06:37.884148', N'Zvichapera');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (107, N'pbkdf2_sha256$1000000$W8PVGMgGH3lTa3I53TdL5W$ne+mU0Dv2yj40ivhGVT/ZNn3hSTkDOBakABPVUCnSaY=', NULL, 0, N'cardwell_makanda', N'Makanda', N'', 0, 1, N'2026-04-08 09:06:38.344879', N'Cardwell');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (108, N'pbkdf2_sha256$1000000$tzqo1BMGX2N4apBPQHBzjc$radGXCO5qCK/LIDAzGcEPROQTPmz3VfB2ktZlQSRDvc=', NULL, 0, N'tafadzwa_tomu', N'Tomu', N'', 0, 1, N'2026-04-08 09:06:38.790313', N'Tafadzwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (109, N'pbkdf2_sha256$1000000$5EqebJ1IZpUGqq6sOaWs1m$8ed2XhSO0WvfTv6FLAXRJadfQw1pK7yTGKI36zrwtlw=', NULL, 0, N'andrew_nyamashuka', N'Nyamashuka', N'', 0, 1, N'2026-04-08 09:06:39.211923', N'Andrew');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (110, N'pbkdf2_sha256$1000000$1DSineOJ7GFuwnEoiQ3Bnw$JYNJ0P7jUNWBb60wvXB7mxmWY8d/o27G6EkmP2ZkE1Q=', NULL, 0, N'james_manyandu', N'Manyandu', N'', 0, 1, N'2026-04-08 09:06:39.635869', N'James');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (111, N'pbkdf2_sha256$1000000$AfY6FpahWwWvvM5EWSxnTM$Qjs0x/ctqcaHm+NtQzGy5uhswBnEXE6PwQAXVX+lFBI=', NULL, 0, N'lincoln_gwengwe', N'Gwengwe', N'', 0, 1, N'2026-04-08 09:06:40.058859', N'Lincoln');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (112, N'pbkdf2_sha256$1000000$INsO6iUevwMBHFqXZr8wiX$3J8D8JU2BiEKcxe3Eqn6tuivPXcgURqOCkAdh2MvA94=', NULL, 0, N'ronward_chibaya', N'Chibaya', N'', 0, 1, N'2026-04-08 09:06:40.486702', N'Ronward');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (113, N'pbkdf2_sha256$1000000$MLg6qwtHspiDkgpPtxcRmP$TYu3nstCw5q7MUeJDfVObJfYYv4fGwNnp8dUPy166vo=', NULL, 0, N'modation_jokonya', N'Jokonya', N'', 0, 1, N'2026-04-08 09:06:40.930908', N'Modation');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (114, N'pbkdf2_sha256$1000000$VcGSammgpa2gEQ5HIgaAvi$LTE03sj1kLqZlKK1We0y8oSDGbRFcPo/yPZcVZMjShY=', NULL, 0, N'admire_kazingizi', N'Kazingizi', N'', 0, 1, N'2026-04-08 09:06:41.476086', N'Admire');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (115, N'pbkdf2_sha256$1000000$nK3J4qwhOh3MbtTjfcEBt5$P/U+GB4dIqx2IfiRmvLyKhktGS3zCOB/RLMmPDp1spw=', NULL, 0, N'walter_sibiya_guyo', N'Sibiya Guyo', N'', 0, 1, N'2026-04-08 09:06:41.905594', N'Walter');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (116, N'pbkdf2_sha256$1000000$orl84ufdoDOhYlcTIR1OXR$FTfq1jxsCPBPHlBFrOmpihD4sOjZ+/wTdg59tFqT4kA=', NULL, 0, N'panganai_mucheche', N'Mucheche', N'', 0, 1, N'2026-04-08 09:06:42.595311', N'Panganai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (117, N'pbkdf2_sha256$1000000$OlXFWfCKQ38Gw2t4qwDWEz$Y3bIU5Kt/TIO+EkvdnYMDE/GcarA17tu9HiPnY25iwM=', NULL, 0, N'leonard_kufakunesu', N'Kufakunesu', N'', 0, 1, N'2026-04-08 09:06:43.378167', N'Leonard');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (118, N'pbkdf2_sha256$1000000$Y8Oe6u0XLFFMn7BlRciyGV$ddiRGAbIJ1G6AximyR+jdT+L0DKuN0ynEehGcDwsWFM=', NULL, 0, N'elton_murambiwa', N'Murambiwa', N'', 0, 1, N'2026-04-08 09:06:44.126396', N'Elton');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (119, N'pbkdf2_sha256$1000000$3dikIcO9oAg3MYpy3Kk3aY$FLeqo6qkgvXjf1L4A8yFy6Uerm0VbgpvjLA+XONaF+4=', NULL, 0, N'leverdellis_mupaya', N'Mupaya', N'', 0, 1, N'2026-04-08 09:06:44.939243', N'Leverdellis');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (120, N'pbkdf2_sha256$1000000$lpfcEJfeuS9H4cZD1Kzjpk$PEBT+RJ3lp7zFvWmIApOmKqMjaFyA6U87GLOf+M6Seo=', NULL, 0, N'tatenda_jinja', N'Jinja', N'', 0, 1, N'2026-04-08 09:06:45.829300', N'Tatenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (121, N'pbkdf2_sha256$1000000$s4014f0Cq8Z0EYFMPRdYuY$i25u2chvwvMENtaMEvEgQ0bRQYbMWXgSk2erKtj40yo=', NULL, 0, N'nyatsungo_paul', N'Paul', N'', 0, 1, N'2026-04-08 09:06:46.638874', N'Nyatsungo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (122, N'pbkdf2_sha256$1000000$LjBUoJxwymnuN108UP2R98$+swUOMUO2KFUmmRdz9vBvE2ThHzRO+4rslPOAe57xns=', NULL, 0, N'samuel_machingauta', N'Machingauta', N'', 0, 1, N'2026-04-08 09:06:47.285692', N'Samuel');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (123, N'pbkdf2_sha256$1000000$ZZdHNYcI1dE0cvlHNjdabR$6brplPVFVLxI9j9uHDpk24W5dgxZAnNegmQvlanwnQg=', NULL, 0, N'lawrence_manyika', N'Manyika', N'', 0, 1, N'2026-04-08 09:06:48.008500', N'Lawrence');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (124, N'pbkdf2_sha256$1000000$Wk9U5Irr3uwrZaxTDzicsB$E4R9VgjFgh75ufgWWplgoKGSUNWoC6Gb6i3Q7Li4HwM=', NULL, 0, N'beauty_kaseke', N'Kaseke', N'', 0, 1, N'2026-04-08 09:06:48.881633', N'Beauty');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (125, N'pbkdf2_sha256$1000000$tLdNEG1VEm1JTCPLMy8g1M$6n2zkhaDvPVn50szUsZ29X72VPhNoOxJQNggR/H97dY=', NULL, 0, N'farai_fusire', N'Fusire', N'', 0, 1, N'2026-04-08 09:06:49.818892', N'Farai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (126, N'pbkdf2_sha256$1000000$2QTmJwmE1b4uT34EXT5NI9$6PjRaaaMCWn7aH7ZJ8klzlFzOkrtLAPCAHCs8dk4SEQ=', NULL, 0, N'john_kaseke', N'Kaseke', N'', 0, 1, N'2026-04-08 09:06:50.710568', N'John');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (127, N'pbkdf2_sha256$1000000$g9gsQNQDwAGnrznStl1zTQ$kcnqKtVfN4SdTt/ukwnGVbgUqAAGb9e9qabZ/qaZtlk=', NULL, 0, N'david_gatsi', N'Gatsi', N'', 0, 1, N'2026-04-08 09:06:51.529324', N'David');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (128, N'pbkdf2_sha256$1000000$99Ofu6IcEZmKvxcpzHVunl$FCBnK++/AAintgj2OOYm9sOtJjdMUoPbNorG8i/jL2U=', NULL, 0, N'nelson_chaziwa', N'Chaziwa', N'', 0, 1, N'2026-04-08 09:06:52.402373', N'Nelson');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (129, N'pbkdf2_sha256$1000000$sqpNYNNNmt3h8uLqYFC59z$L5KZ0nrGQ5uJulBGraR3v1ufssshRDW3lsCwHqRsy+g=', NULL, 0, N'arthur_mhungu', N'Mhungu', N'', 0, 1, N'2026-04-08 09:06:53.393845', N'Arthur');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (130, N'pbkdf2_sha256$1000000$w4mIq5jptX4V6MWy9KOfbM$tQXyTU62GRZ/nWpT95SaacHIW7Tq/iL1lL8kHv38Bkg=', NULL, 0, N'tafadzwa_zinzada', N'Zinzada', N'', 0, 1, N'2026-04-08 09:06:54.411605', N'Tafadzwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (131, N'pbkdf2_sha256$1000000$XryeFPIZXq0J3JvuO14w3n$iPN8mR4mBthiug0qcBZKT9PVA20F/VB7GOcfwcjWZwU=', NULL, 0, N'onias_kahuni', N'Kahuni', N'', 0, 1, N'2026-04-08 09:06:55.273993', N'Onias');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (132, N'pbkdf2_sha256$1000000$0eMYRpSi7wG2JOqJVm5Ugr$hbPNEJUnreyRUa283aUdRqgIRGhJoGUuw+5vUwMN9Ps=', NULL, 0, N'tariro_chitsamba', N'Chitsamba', N'', 0, 1, N'2026-04-08 09:06:56.016563', N'Tariro');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (133, N'pbkdf2_sha256$1000000$kR5nO8kuCzaTDyT1BXS9DZ$ivbam8vvqlwUufHOK8MdS4Hv+fr6Qcb7b/tebDcKaWg=', NULL, 0, N'godknows_phiri', N'phiri', N'', 0, 1, N'2026-04-08 09:06:56.787897', N'Godknows');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (134, N'pbkdf2_sha256$1000000$fUpXzBrqCGznVfEomUFY2A$wISUdoxIqTkBvWo98mkv/nrRb3TAtpJ9M/hc9HLBmRk=', NULL, 0, N'markson_gutusa', N'Gutusa', N'', 0, 1, N'2026-04-08 09:06:57.634772', N'Markson');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (135, N'pbkdf2_sha256$1000000$8EGE1w2gOSUYWvKRziZfQu$O80QTbikThRbs2P0XkIDRF+dK4ooIIDqWjtm/Yj8EcI=', NULL, 0, N'roshem_chanhuhwa', N'Chanhuhwa', N'', 0, 1, N'2026-04-08 09:06:58.417294', N'Roshem');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (136, N'pbkdf2_sha256$1000000$8CctYRl2M7ZVV3MZmx05ba$UA/XYD6IDBq/Nb04u/H3oNIH8DM2p218wCpD4YOeghU=', NULL, 0, N'marimbe_tinotenda', N'Tinotenda', N'', 0, 1, N'2026-04-08 09:06:59.286178', N'Marimbe');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (137, N'pbkdf2_sha256$1000000$HZQTAqiKiSrehuFAThRnI4$BpCMaZQ5NwtiD0HfS15CU8xJr6aoD7Aomc1LuFRkqI0=', NULL, 0, N'vhurande_tendai', N'Tendai', N'', 0, 1, N'2026-04-08 09:07:00.252767', N'Vhurande');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (138, N'pbkdf2_sha256$1000000$ArU8LV3oKmK0wauN6XbFuE$qdwK07GYjel2ycTO7NgyklufYJhSh+soBCvTlhJYWTY=', NULL, 0, N'clifford_kuforomi', N'Kuforomi', N'', 0, 1, N'2026-04-08 09:07:01.149616', N'Clifford');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (139, N'pbkdf2_sha256$1000000$poBT1v5et5xkHWFjYcujqW$DstSzNC/sP/XHxPW0InCAogVsHh+Kuehc6QQXQY0RQo=', NULL, 0, N'muradzikwa_gararikai', N'Gararikai', N'', 0, 1, N'2026-04-08 09:07:01.951960', N'Muradzikwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (140, N'pbkdf2_sha256$1000000$0dL4hvldEHaDJHDrYvr09F$XZSuMchQD5oDW8DdNrlOZhjl51GiqC1tmEsBznQMn4g=', NULL, 0, N'francis_f_penzura', N'F Penzura', N'', 0, 1, N'2026-04-08 09:07:02.782234', N'Francis');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (141, N'pbkdf2_sha256$1000000$z8SglQVVcGUS5FRWriH4EI$ft/oRpHOYQe2zjkGDEg6SM1IQCQONstvM9UgrcUqeQk=', NULL, 0, N'tendaupenyu_tapera', N'Tapera', N'', 0, 1, N'2026-04-08 09:07:03.595272', N'Tendaupenyu');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (142, N'pbkdf2_sha256$1000000$xTCPuU3l23Krc6IarM646I$O4O3PDaa/1wwlcHPxFVcg/pTbQ3wtyEMC6m6ziWasYU=', NULL, 0, N'mashamba_godwin', N'Godwin', N'', 0, 1, N'2026-04-08 09:07:04.420365', N'Mashamba');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (143, N'pbkdf2_sha256$1000000$Uf07DuP0umsTDHMFwZ3tgB$wlMDy+YMqHG3DO5lYNrdVCsA9n5AybYHRo4zQi7Qaj8=', NULL, 0, N'zivanai_wonder', N'Wonder', N'', 0, 1, N'2026-04-08 09:07:05.351180', N'Zivanai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (144, N'pbkdf2_sha256$1000000$IrPCCrWF5Ed6RsIKS5Q4qL$IM/cW9IwmPH1mreKRm9lrjykXH9cHOusATSVAEd3xh8=', NULL, 0, N'tatenda_chasumba', N'chasumba', N'', 0, 1, N'2026-04-08 09:07:06.196086', N'Tatenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (145, N'pbkdf2_sha256$1000000$fXn5uaFjhdOpQn2M0DRhe0$PDgwIzDrqT+hq+5rtKkTS3cSHb6EF+y1M7j6DNt0he8=', NULL, 0, N'moyo_hampton_b', N'Hampton B', N'', 0, 1, N'2026-04-08 09:07:07.082081', N'Moyo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (146, N'pbkdf2_sha256$1000000$Tsw2lViaGSfadcT3NPie5N$FgOpmeeXihTLYTaGVGiaErwOpvjh63FgQuH01bRzlXk=', NULL, 0, N'steven_mpofu', N'Mpofu', N'', 0, 1, N'2026-04-08 09:07:08.102071', N'Steven');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (147, N'pbkdf2_sha256$1000000$LwzUG3YuPWjBAU5WQmJuVI$qnhkV7AlpMWe3HN7SXBUlOkLkR+z5gUoyo/JdzCljl0=', NULL, 0, N'mumanyi_harrison', N'Harrison', N'', 0, 1, N'2026-04-08 09:07:08.846481', N'Mumanyi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (148, N'pbkdf2_sha256$1000000$qPjIABtNqBXLyceVBkhVhh$juyhXJ37Hh3zozKMybm7uoKS7H3k5i3ddDPF4zFZkCY=', NULL, 0, N'magwaza_prosper', N'Prosper', N'', 0, 1, N'2026-04-08 09:07:09.605418', N'Magwaza');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (149, N'pbkdf2_sha256$1000000$rKbGDJXQIahS8pzNo14onb$rznGE0QoqQkLCpKJNFn/7OTMZ+a39o+CPC9qYOgbtZk=', NULL, 0, N'ndlovu_solomon', N'Solomon', N'', 0, 1, N'2026-04-08 09:07:10.365671', N'Ndlovu');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (150, N'pbkdf2_sha256$1000000$ubfrEz16lIWSHzkYv1zg4P$LTHsUejWSGm2iQJCLkWzx50vIsKfCCu7O2rfSY0Ouks=', NULL, 0, N'danmore_jatakalula', N'Jatakalula', N'', 0, 1, N'2026-04-08 09:07:11.118536', N'Danmore');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (151, N'pbkdf2_sha256$1000000$J5gH1SdlN7pxhh7Xd7N2dC$f3nquLEbI12flY5wzRR6PXmdfm43o+U+DyNC6uD80c8=', NULL, 0, N'tafadzwa_farai_karidza', N'Farai Karidza', N'', 0, 1, N'2026-04-08 09:07:11.869605', N'Tafadzwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (152, N'pbkdf2_sha256$1000000$rHYBKhcshKAfdK0lOlmayg$jtyiNF0ccCbN47O4xpeRJNZD24S5iehNJWwD57HrDQY=', NULL, 0, N'collen_govo', N'Govo', N'', 0, 1, N'2026-04-08 09:07:12.653047', N'Collen');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (153, N'pbkdf2_sha256$1000000$LgVvVQmvbjiI6Uheu7aKfp$eNEcrOkSK3lUpyaEuGKiK0OfEQr8QbPLLUSfx7T854o=', NULL, 0, N'shawarira_maxwell', N'Maxwell', N'', 0, 1, N'2026-04-08 09:07:13.500866', N'Shawarira');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (154, N'pbkdf2_sha256$1000000$mr5Iop2FAwpXCdM1srqtN0$suNVRZNBFPuLx0zL+Gniki+4i3K96ZvJsO/zaHYlEeo=', NULL, 0, N'levy_mufuka', N'Mufuka', N'', 0, 1, N'2026-04-08 09:07:14.394156', N'Levy');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (155, N'pbkdf2_sha256$1000000$7wiyhZ6d3ABzsPJMSgMP34$KIiBSgh8QfRLsScFct4LdNakq8TGo5EYNUAt0eRu12E=', NULL, 0, N'mondreck_chimanga', N'Chimanga', N'', 0, 1, N'2026-04-08 09:07:15.300012', N'mondreck');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (156, N'pbkdf2_sha256$1000000$w1AuXcgbGD9fL2Ria04Kaa$5PICKRBSzPGpUKVKafajLgcVbY88+T3hQo4JSWCWxK8=', NULL, 0, N'ahmed_salim_komichi', N'Salim Komichi', N'', 0, 1, N'2026-04-08 09:07:16.224032', N'Ahmed');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (157, N'pbkdf2_sha256$1000000$NnBRzSkRGkD8uTrZdAKWUu$ECTyCIYt17U/8UjmKgFRV+h79Ws6/w8DE+CwphV6JK8=', NULL, 0, N'makisi_goodluck', N'Goodluck', N'', 0, 1, N'2026-04-08 09:07:17.093825', N'makisi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (158, N'pbkdf2_sha256$1000000$gNCRHAhqT0DLse0DHWDVS6$zQ5rXlI2EbrP+up6gGkYk1zGsVhYvh75psHtiaMc0JM=', NULL, 0, N'last_tsandura', N'Tsandura', N'', 0, 1, N'2026-04-08 09:07:17.929869', N'Last');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (159, N'pbkdf2_sha256$1000000$Abs2T5YZ8xWyiWCASFxXax$p9XWmlToC61vOsOGZPO0J6FMhnpSPCJTg2cIrNIi9nw=', NULL, 0, N'gibson_chikwinya', N'Chikwinya', N'', 0, 1, N'2026-04-08 09:07:18.783428', N'Gibson');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (160, N'pbkdf2_sha256$1000000$Ygg06YLtjK26eOZmx4YCVJ$1F5IlLH1cXDPBogIyQFl/pntD1DCZWqnOib2/47K/qY=', NULL, 0, N'tariro_dihori', N'Dihori', N'', 0, 1, N'2026-04-08 09:07:19.606221', N'Tariro');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (161, N'pbkdf2_sha256$1000000$Qq3gQWcN7CVqycMHhQwiDL$74256Hn1463cnGdRg3+gBvl5k/RB0mjztpzRxnFRWVs=', NULL, 0, N'aaron_mushanje', N'Mushanje', N'', 0, 1, N'2026-04-08 09:07:20.327078', N'Aaron');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (162, N'pbkdf2_sha256$1000000$QtntflhYlQc5DAjUgKJwgH$pSzX9GfiLu9QUGVFBi1tpVMbqOjgaCG5mPc4RAPSlkw=', NULL, 0, N'musokeri_enock', N'Enock', N'', 0, 1, N'2026-04-08 09:07:21.172402', N'Musokeri');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (163, N'pbkdf2_sha256$1000000$CPvXaXvI9qQN1es40HWArO$nx2P7ekO0cBT9g2cQEg/V0i/lOYdhCUiexitWxPUSX4=', NULL, 0, N'wilfred_mvula', N'Mvula', N'', 0, 1, N'2026-04-08 09:07:22.091708', N'Wilfred');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (164, N'pbkdf2_sha256$1000000$r5CbiBZm5QFBTlqcZWCXkb$qgAJz0nkSdJer1Sg/j/OLcKne7xPtC+peORYEHx3Ldg=', NULL, 0, N'nyasha_chikwayi', N'Chikwayi', N'', 0, 1, N'2026-04-08 09:07:22.910565', N'Nyasha');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (165, N'pbkdf2_sha256$1000000$wk2DYiUlV7stbtaCw2ZFey$O5RyrkIQKY/o9qwf+H0SL9tLBP4hrd5HO9SzUCqVX0M=', NULL, 0, N'vincent_mariga', N'Mariga', N'', 0, 1, N'2026-04-08 09:07:23.690013', N'Vincent');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (166, N'pbkdf2_sha256$1000000$LOZO5fUCDEp6x6tbkxt4tS$SPCJ4/2+Rpr8rEuOF/aVyPqFhtbTCfVnDCf6cq2KJ6o=', NULL, 0, N'dickson_chiwaya', N'Chiwaya', N'', 0, 1, N'2026-04-08 09:07:24.460598', N'Dickson');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (167, N'pbkdf2_sha256$1000000$e7DlXI7y5f1hUDlNSu0j3r$Kn2u+jEeh2nSetfuVmc+6dEOan0CJLeoxQvWaaHknlE=', NULL, 0, N'witness_musenda', N'Musenda', N'', 0, 1, N'2026-04-08 09:07:25.189394', N'Witness');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (168, N'pbkdf2_sha256$1000000$Br3gK3U5VoRxRXmNG9Us86$b67364b/dYFuIPRV8PxbuTCGozPz3/8KEVnPYrd3Yvc=', NULL, 0, N'mutukwa_tobias_b', N'Tobias B', N'', 0, 1, N'2026-04-08 09:07:25.988797', N'Mutukwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (169, N'pbkdf2_sha256$1000000$pzJQHO8L9ekOHjEtvRDTGp$da8p9RqjoyIa7n+eZIzpwTRiLK1PDoOUkG8DX7wWxY0=', NULL, 0, N'trust_makombe', N'Makombe', N'', 0, 1, N'2026-04-08 09:07:26.635768', N'Trust');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (170, N'pbkdf2_sha256$1000000$kwJYUOQtdJoSQiC3WNhqtw$R1Du3prg+398TL9cnTr/2W4Ml9giXVbGtxH0BPBLx4E=', NULL, 0, N'mungwini_necodemo', N'Necodemo', N'', 0, 1, N'2026-04-08 09:07:27.468977', N'Mungwini');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (171, N'pbkdf2_sha256$1000000$vxpuj70hfTCNKOUOpRdaag$d08adS5P37RCUCSvDRwyB69Xl8bNK/25vFP7rFgrFyg=', NULL, 0, N'muzuza_edson', N'Edson', N'', 0, 1, N'2026-04-08 09:07:28.417364', N'Muzuza');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (172, N'pbkdf2_sha256$1000000$IGq2pJffmndkLjkGC9gcnO$Mt/6TpIKgIjdcUdgaBbBqHkldA0+3Xw18RDXdqrklFo=', NULL, 0, N'owen_shumba', N'SHUMBA', N'', 0, 1, N'2026-04-08 09:07:29.178989', N'OWEN');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (173, N'pbkdf2_sha256$1000000$gB5spFXZfcotdW5bHd8EX9$eU2W2yA2cdvIxse/DDsaZSIM4TGU5FNvpdAdOicBky8=', NULL, 0, N'donald_chikoto', N'Chikoto', N'', 0, 1, N'2026-04-08 09:07:30.111347', N'Donald');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (174, N'pbkdf2_sha256$1000000$iNoqbaJDZlG1Q0mSWvBOSv$h+16J3T9IYFLU4URrM5HGk7T6/DdxNgN8MN52uTLRs0=', NULL, 0, N'machingura_calisto', N'Calisto', N'', 0, 1, N'2026-04-08 09:07:30.923338', N'Machingura');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (175, N'pbkdf2_sha256$1000000$h9KbSIE1SNOVvBDBn1zZRu$8QxqZOrD43Z2fLOVvxHziFd8bkPaUpR4GNJ7KTJ4/bU=', NULL, 0, N'mavhiya_rangarirai', N'Rangarirai', N'', 0, 1, N'2026-04-08 09:07:31.738035', N'Mavhiya');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (176, N'pbkdf2_sha256$1000000$zbQLArNzXxvoySBK8TSzsU$2Xg1olsHV84O72RmYZb6lLaBj7iCUurXMnZ5m9YzAYQ=', NULL, 0, N'trust_kamvura', N'Kamvura', N'', 0, 1, N'2026-04-08 09:07:32.437805', N'Trust');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (177, N'pbkdf2_sha256$1000000$FHiPsrpuUi7cRwr2T4l2Eo$mx7Ix71wP+3BWmmcMnv6fdU27w8qqZL+9UGUvlKN60g=', NULL, 0, N'chirandata_rabson', N'Rabson', N'', 0, 1, N'2026-04-08 09:07:33.277775', N'Chirandata');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (178, N'pbkdf2_sha256$1000000$VYaoMH1QZkeqji0T25Lwhf$mBKDoR8eczxkEJyODy/+NFTD1OXyHpe88mOwLk62ZLw=', NULL, 0, N'livombo_progress', N'Progress', N'', 0, 1, N'2026-04-08 09:07:34.020535', N'Livombo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (179, N'pbkdf2_sha256$1000000$ppeoTQ0smyDpXXmyBtxOxU$v90U8pImpk0relddAPPMZ2AZyvjv05Ai72RTq/HVDsk=', NULL, 0, N'mupisa_johannes', N'Johannes', N'', 0, 1, N'2026-04-08 09:07:34.751330', N'Mupisa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (180, N'pbkdf2_sha256$1000000$T7sjkXzvNYbZD2UFLe6szf$1+hWRrhDy4f/VirjJOvXshr705BSpsnSBhbIsBh8gK4=', NULL, 0, N'mataruse_gift', N'Gift', N'', 0, 1, N'2026-04-08 09:07:35.535120', N'Mataruse');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (181, N'pbkdf2_sha256$1000000$Em1ksCHxETEIPgcMeqLTvT$xonU8DiLIwxIF/7CdEyi7dULy14nh2WavRsGWS7bp14=', NULL, 0, N'sungai_friday', N'Friday', N'', 0, 1, N'2026-04-08 09:07:36.306024', N'Sungai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (182, N'pbkdf2_sha256$1000000$JGRD5sk6Sqi2c6YRG3ppFw$PQKRlqPnIuRSiNhde09/0ZWf6ac2SHAig/TqgAggPlE=', NULL, 0, N'emmanuel_chinyanganya', N'Chinyanganya', N'', 0, 1, N'2026-04-08 09:07:37.058125', N'Emmanuel');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (183, N'pbkdf2_sha256$1000000$NCeo3kDMMpkAulRSe78r9R$3T4SGATJsvcV5gB/GYxU3oVla9eFpcOSJgtveXQuWI0=', NULL, 0, N'charinda_tinashe', N'Tinashe', N'', 0, 1, N'2026-04-08 09:07:37.715804', N'Charinda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (184, N'pbkdf2_sha256$1000000$i1jVUCvKoRrYjhPkOws2sp$oxdfvmNR2FwTHMndheS5HNT2uq6PvDt+NTMbhYiWxpc=', NULL, 0, N'judge_rondo', N'Rondo', N'', 0, 1, N'2026-04-08 09:07:38.573619', N'Judge');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (185, N'pbkdf2_sha256$1000000$gwR0ovTtNuDbp0vhkLreEj$dVirAHiLmlpJR5UjQkJdgY8geqoyLuIJZFPrR+zZk6A=', NULL, 0, N'shiri_david', N'David', N'', 0, 1, N'2026-04-08 09:07:39.445525', N'Shiri');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (186, N'pbkdf2_sha256$1000000$nGywMlPMIo3J9mWm7ZPX4S$Oi32+tvIdIfn/ip1MC40lvvZcMpVLQ8nZqYXF4UAJQU=', NULL, 0, N'moyo_tinashe', N'Tinashe', N'', 0, 1, N'2026-04-08 09:07:40.533183', N'Moyo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (187, N'pbkdf2_sha256$1000000$sjYLX38efzghBTPcfWEWeQ$kOgoVvL1EUWwq4w/CDyecFUHCd358HPJjyRPXQbH/WY=', NULL, 0, N'mukariwafa_grey', N'Grey', N'', 0, 1, N'2026-04-08 09:07:41.297074', N'Mukariwafa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (188, N'pbkdf2_sha256$1000000$gHYtGl733NJQejHRaekL7B$CZfcbIVRBncwrgOK3a22EohVk+vDo1lYVukvXMg+oTA=', NULL, 0, N'eckewell_madzivamutse', N'Madzivamutse', N'', 0, 1, N'2026-04-08 09:07:42.021880', N'Eckewell');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (189, N'pbkdf2_sha256$1000000$RGVgg3iTgAOr8odYnZXjyQ$hioiGtsM2ju52xSmZ7xXjlcw+y8w/OIqmGcYqpbVBVQ=', NULL, 0, N'mawire_nicholas', N'Nicholas', N'', 0, 1, N'2026-04-08 09:07:42.758454', N'Mawire');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (190, N'pbkdf2_sha256$1000000$byWWJz84bRq5kPswHUtLKb$kBdtehD4KiO1eP+cTAHTTygZ3hxBvFye13RTmhcGVbg=', NULL, 0, N'jannis_kuchinani', N'Kuchinani', N'', 0, 1, N'2026-04-08 09:07:43.584292', N'Jannis');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (191, N'pbkdf2_sha256$1000000$WWjFCOaAmnHaKHh3XWCzd4$08Vq9e+ndh8D9bemSzlc2TLEkcwSEas2QBBXfZgqnNo=', NULL, 0, N'tsumisa_saviours', N'Saviours', N'', 0, 1, N'2026-04-08 09:07:44.468924', N'Tsumisa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (192, N'pbkdf2_sha256$1000000$ub9jWABE3gqfBPkb4kKdln$Hgwl8p+pc1ahyuqmm/NUpRwg1+ZuSiuL3q895ZMTGSU=', NULL, 0, N'memelord_chikasha', N'Chikasha', N'', 0, 1, N'2026-04-08 09:07:45.398276', N'Memelord');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (193, N'pbkdf2_sha256$1000000$OtsI1xuzf0NOwnzBYyrET7$Mch5o2iDvPqZwBi0KoIzduxmnp+zuF+pq7cGtlLauFA=', NULL, 0, N'sithole_charles', N'Charles', N'', 0, 1, N'2026-04-08 09:07:46.172036', N'Sithole');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (194, N'pbkdf2_sha256$1000000$Nl0jDHQyV6Pa5Jp4h82mhk$dMClMXjjQD3+3ZElCw9P9g6dlIY46YZy51/BQLwzbxw=', NULL, 0, N'tinotenda_matemera', N'Matemera', N'', 0, 1, N'2026-04-08 09:07:47.357847', N'Tinotenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (195, N'pbkdf2_sha256$1000000$r3nUf3DDZFV652LHlvDCfS$6WM5iZdVbm8AnZTTBgD796DY0X4BBD0pfmKWLcW9Zus=', NULL, 0, N'western_wisani', N'Wisani', N'', 0, 1, N'2026-04-08 09:07:49.166609', N'Western');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (196, N'pbkdf2_sha256$1000000$VktyQ7bN7c5VvduD8HgwfP$y/tA96FgPV7Qb2dGzJSX1twrmHZ3ICu54dvwZVKw5vM=', NULL, 0, N'gumbo_godfrey', N'Godfrey', N'', 0, 1, N'2026-04-08 09:07:50.567346', N'Gumbo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (197, N'pbkdf2_sha256$1000000$weqSbgT1K0TEFWiFLU4tKn$1gdumWhNEoI9mdxa7pqVkASmDSgtv18mxZ+7N0e8d0U=', NULL, 0, N'matuvi_silas', N'Silas', N'', 0, 1, N'2026-04-08 09:07:51.689284', N'Matuvi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (198, N'pbkdf2_sha256$1000000$864bT8GNrYVBsFh6Q4BRYJ$ycN5oAlRYTNyJ0XWMh2vDK7XEzwYYXifss3lNzh0doI=', NULL, 0, N'maguraushe_zvirevo', N'Zvirevo', N'', 0, 1, N'2026-04-08 09:07:52.753025', N'Maguraushe');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (199, N'pbkdf2_sha256$1000000$t2cp3SjjEDreQ3Bj9xdGRb$ZNbjPVVbWxmrlZWRXuEA13IgMCYJCML5U2Uq6qfWwks=', NULL, 0, N'tafara_machingambi', N'Machingambi', N'', 0, 1, N'2026-04-08 09:07:53.795234', N'Tafara');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (200, N'pbkdf2_sha256$1000000$j3PEqxIWdbXUAOXAUUO0Ji$VoFU65NVE3zmzHfvL4fEFaQz81qOqHip4NWT1zFN2h8=', NULL, 0, N'trust_nyika', N'Nyika', N'', 0, 1, N'2026-04-08 09:07:55.203506', N'Trust');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (201, N'pbkdf2_sha256$1000000$F5aXAdC0aySIxHIcl4ByvJ$krJAKc/6cjic2PHqZlQjMnl+IbQYi1mWPbi0GsCNKhE=', NULL, 0, N'kudakwashe_sibanda', N'Sibanda', N'', 0, 1, N'2026-04-08 09:07:56.304286', N'Kudakwashe');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (202, N'pbkdf2_sha256$1000000$2wWcSOcLJlv6hFgpNkZGx6$sS5xt9JmY63Uu/WgxjPlVpiw4PuLDe2ObuJi1eAiAgE=', NULL, 0, N'hughes_muzopa', N'Muzopa', N'', 0, 1, N'2026-04-08 09:07:57.367692', N'Hughes');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (203, N'pbkdf2_sha256$1000000$125PaoSyTBa14LjH95d8Dw$YvbmfnsW2F6bbk9EX2hT/WcENqYp+H+rDtUSNiwj0Qk=', NULL, 0, N'lucky_tambo', N'Tambo', N'', 0, 1, N'2026-04-08 09:07:58.342052', N'Lucky');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (204, N'pbkdf2_sha256$1000000$hsBVBo4HdDDz8YopYG32TI$8+FoIDn5trga9S/CK+hcPaLgyMF6fDfafF4wUmAh72E=', NULL, 0, N'ndlovu_fortune', N'Fortune', N'', 0, 1, N'2026-04-08 09:07:59.304302', N'Ndlovu');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (205, N'pbkdf2_sha256$1000000$lYGn8jQL2hiF8L752I1zfN$NS2ZNo+HxUD1uMxCu/VoGUimXLfaOn5S+lE+ra3n1nA=', NULL, 0, N'thembani_khumalo', N'Khumalo', N'', 0, 1, N'2026-04-08 09:08:00.486111', N'Thembani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (206, N'pbkdf2_sha256$1000000$hqn7XjFpu66wCizlCQ4Z2f$0WqNQbPd9RRvQX+POEEKT9Ri6/bDyXVfy/biDdbivPQ=', NULL, 0, N'picot_moyo', N'Moyo', N'', 0, 1, N'2026-04-08 09:08:01.589467', N'Picot');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (207, N'pbkdf2_sha256$1000000$0zMY0t13CWFFvONNcIdRb1$wpG4kzacgm++k2Wb4nCODMBGklBGXQdUk83YgZQOSes=', NULL, 0, N'fezile_dube', N'Dube', N'', 0, 1, N'2026-04-08 09:08:02.961160', N'Fezile');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (208, N'pbkdf2_sha256$1000000$ffOVSJog5VNh7QwEGwSyMe$upLoEjJHeZGYu+29UX3UkXDpMcPFpfQhccarI9EtRZ4=', NULL, 0, N'benson_shoko', N'Shoko', N'', 0, 1, N'2026-04-08 09:08:03.976135', N'Benson');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (209, N'pbkdf2_sha256$1000000$muqfRDa1mrVoH3JcpBp0GJ$tZF4MtrBkN6DhW6AbMmMbkSRqq750Abt6J2QzCZP0ho=', NULL, 0, N'sipho_mahlangu', N'Mahlangu', N'', 0, 1, N'2026-04-08 09:08:04.715375', N'Sipho');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (210, N'pbkdf2_sha256$1000000$r3bumYW2ShooV9izJOOlzO$zuWoaaA3d3N8hLBzp34WgljFBute4bWgy+epe6hB1kE=', NULL, 0, N'thabani_ndlovu', N'Ndlovu', N'', 0, 1, N'2026-04-08 09:08:05.643702', N'Thabani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (211, N'pbkdf2_sha256$1000000$2dEW9OvSVw3WlfOkfg1Vbc$Bunrf+naKEMjHAcqUCN1sQHfMAohDt4Fpy7q4tGt7QQ=', NULL, 0, N'devine_muchimba', N'Muchimba', N'', 0, 1, N'2026-04-08 09:08:06.454985', N'Devine');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (212, N'pbkdf2_sha256$1000000$RdzTaeG3An8kaQlxRi0jO6$ynDeji120YFFNu2mNIMv5ScxW9nGvrMkoy60JxKSosk=', NULL, 0, N'alexander_munsaka', N'Munsaka', N'', 0, 1, N'2026-04-08 09:08:07.368701', N'Alexander');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (213, N'pbkdf2_sha256$1000000$WZWAR9HQSXmvrKZeJByejx$hqSPtE1WgcDrmv+7KmKM6U7iw1IW8LCO5M2epqtC+Pw=', NULL, 0, N'abednico_mukhuli', N'Mukhuli', N'', 0, 1, N'2026-04-08 09:08:08.301060', N'Abednico');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (214, N'pbkdf2_sha256$1000000$9v7M8y2lQSWMqQENoGgHTs$jNOsMJtXup3L1e15cPwbM7t5WFKkfEtXFAwT4TDhUtI=', NULL, 0, N'sehlelo_sibanda', N'Sibanda', N'', 0, 1, N'2026-04-08 09:08:09.121239', N'Sehlelo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (215, N'pbkdf2_sha256$1000000$UcxZsH9UJVSm0KOGf81dyH$hKr2b3a6ZQ1mPhkdd1v2Ybxs4rKTBeBX1sPGGG+sgSs=', NULL, 0, N'thabani_sibanda', N'Sibanda', N'', 0, 1, N'2026-04-08 09:08:09.907878', N'Thabani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (216, N'pbkdf2_sha256$1000000$Sp50uGPgCssDEfv6AZ156L$ukjXvoxLdqmFOI5jxwqhMWJy8voGHNMyO/6LgSO4uQM=', NULL, 0, N'taurai_dube', N'Dube', N'', 0, 1, N'2026-04-08 09:08:10.738749', N'Taurai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (217, N'pbkdf2_sha256$1000000$iDxHv0mEMdtpj7fGpgum88$XULMSYdH5EeTjsoQVBjcKdhZjFR/PQYKXwLJQNcaTRs=', NULL, 0, N'fuzane_langelihle', N'Langelihle', N'', 0, 1, N'2026-04-08 09:08:11.815168', N'Fuzane');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (218, N'pbkdf2_sha256$1000000$y3cWCGQwZNCJwWkq8WjVJI$YlvmH8vkCETQ2EihInN3QJiPhY1E/6POnlYxxaRZESY=', NULL, 0, N'njongoenhle_moyo', N'Moyo', N'', 0, 1, N'2026-04-08 09:08:12.757425', N'Njongoenhle');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (219, N'pbkdf2_sha256$1000000$sMPP5mBRf15Q3rrw6XoWHC$pBzK4PZqOZtspcikW0vvYkjzRpqT+Z6ABISHh15yyZM=', NULL, 0, N'mendrick_moyo', N'Moyo', N'', 0, 1, N'2026-04-08 09:08:13.922332', N'Mendrick');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (220, N'pbkdf2_sha256$1000000$ndSuJnDKEWg3jufEXhwAgo$UicNupsbUY1ck0AIMfV6YFwa0Sc2npx6Cdzacp8Mzf8=', NULL, 0, N'lubasi_mathe', N'Mathe', N'', 0, 1, N'2026-04-08 09:08:14.828095', N'Lubasi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (221, N'pbkdf2_sha256$1000000$uaiYJ8yhTR48TuKQ5kC6Au$9TSpwseIFDul7iq7bQzUJCLm7N97K469/FQMMwqoEN0=', NULL, 0, N'jaison_moyo', N'Moyo', N'', 0, 1, N'2026-04-08 09:08:15.718286', N'Jaison');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (222, N'pbkdf2_sha256$1000000$8f3OR6NeCkJLwPWAZBZ9s6$Yqxl9oaQ84L9Ilna1Ly1XjYFYgz9K2ock7RUuY5YMLA=', NULL, 0, N'rodwell_vundla', N'Vundla', N'', 0, 1, N'2026-04-08 09:08:16.566403', N'Rodwell');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (223, N'pbkdf2_sha256$1000000$RuVjhU2BmrAQLMqjTAA4ob$dLkL2NxZr+VABa1WVJDdMAPUTEiV/scJkKKcHpcqD6s=', NULL, 0, N'blessed_taruvinga', N'Taruvinga', N'', 0, 1, N'2026-04-08 09:08:17.369683', N'Blessed');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (224, N'pbkdf2_sha256$1000000$GczxdLf3Lah7v4wJHrU3s2$uNn2V4vjXlZD2q15ydiJ2xQIEIgYRQhtqm2RcqCsoq0=', NULL, 0, N'farfrea_jonathan', N'Jonathan', N'', 0, 1, N'2026-04-08 09:08:18.169413', N'Farfrea');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (225, N'pbkdf2_sha256$1000000$zVzCENRGhg60jW1Ecs4QYt$rsKE5YWuzlQybwSXyj7H22AG7yTGus7UZDXEUQaTmyQ=', NULL, 0, N'doubt_sibanda', N'Sibanda', N'', 0, 1, N'2026-04-08 09:08:18.908271', N'Doubt');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (226, N'pbkdf2_sha256$1000000$wXo4I1YkSsP6F1nHIUKPis$f6CP324S+R59u0b6ZsmnrHan4tcbRVV+efiBpSCfbvM=', NULL, 0, N'mavelous_mabhena', N'Mabhena', N'', 0, 1, N'2026-04-08 09:08:19.820259', N'Mavelous');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (227, N'pbkdf2_sha256$1000000$KBKt6GILtZzP3uu2YkkU3K$uZwANrDZiIQYqo7KLnR8pECN+DlFpZ1r3x/R6LihG0w=', NULL, 0, N'martin_dube', N'Dube', N'', 0, 1, N'2026-04-08 09:08:20.537358', N'Martin');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (228, N'pbkdf2_sha256$1000000$jmtYNh4jcflpMzKO4cnzwj$7Lk3XMlE9ieG5yN93JBLim+nd6VpAMMUhZVEVsFr6GY=', NULL, 0, N'wiseman_mukwena', N'Mukwena', N'', 0, 1, N'2026-04-08 09:08:21.219206', N'Wiseman');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (229, N'pbkdf2_sha256$1000000$vb7QV0yO6wgI7Rv6JBFV7W$zi3M7nbvQt4vg/Zf4XXE0wWst+ffW1efns2pT5OfpCQ=', NULL, 0, N'jaison_mangena', N'Mangena', N'', 0, 1, N'2026-04-08 09:08:22.092283', N'Jaison');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (230, N'pbkdf2_sha256$1000000$YE4NeWqiQahkHmlcTUS4pU$oVL4SdgWoEprWiljlMr/ahc9W+EQJFqvtPf2d9efkFk=', NULL, 0, N'lerato_noko', N'Noko', N'', 0, 1, N'2026-04-08 09:08:22.932322', N'Lerato');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (231, N'pbkdf2_sha256$1000000$wAxdubx6b6xUUuVC05ySIL$ByhAsYJe7n6vlYEIUiWxjV5KiBN2PDGQfDH1Xnfo77g=', NULL, 0, N'nathan_muleya', N'Muleya', N'', 0, 1, N'2026-04-08 09:08:23.702912', N'Nathan');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (232, N'pbkdf2_sha256$1000000$62AVIz9UjWlNEBmOOloZlO$Z+jJVVGCtvvGJz7yUJ3zNAhhhGzBlxv6Sz8MgbnOKa0=', NULL, 0, N'mabutho_siziba', N'Siziba', N'', 0, 1, N'2026-04-08 09:08:24.568773', N'Mabutho');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (233, N'pbkdf2_sha256$1000000$cwV98qRkAyC922pNYuYhxV$+fJ7PUC830bu4u0bF2Sp9SqV98LPOMO1ub7umpCUzEM=', NULL, 0, N'fredrick_ncube', N'Ncube', N'', 0, 1, N'2026-04-08 09:08:25.389357', N'Fredrick');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (234, N'pbkdf2_sha256$1000000$8tFXWeG6tGrt7Hds6p7Ywj$IPyk9WcanmuWTBaVt/6trZ82oIMNbbWrsKLbL08ijYw=', NULL, 0, N'majoni_mudadisi', N'Mudadisi', N'', 0, 1, N'2026-04-08 09:08:26.246428', N'Majoni');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (235, N'pbkdf2_sha256$1000000$9vzc2E9elnOsqRVHyTbaDF$bKb4ZZwvKgloRRDz4D/ZFfB4YyJuneyxmW+XNOHAVZw=', NULL, 0, N'dumolwenkosi_nyoni', N'Nyoni', N'', 0, 1, N'2026-04-08 09:08:26.931279', N'Dumolwenkosi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (236, N'pbkdf2_sha256$1000000$TO633scSymqKop0fsJNbLL$XtEfaHdGlAzEbG6pWbA1ESfgfhJsWuobjIwiy69ONXU=', NULL, 0, N'similo_siziba', N'Siziba', N'', 0, 1, N'2026-04-08 09:08:27.963778', N'Similo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (237, N'pbkdf2_sha256$1000000$cUpvmWDYLL3dyWL5ZK9DPQ$PsCPn7z4oomLC4WlNzQc9IZiGkrFf2SZBDi2DwWh4X0=', NULL, 0, N'mthandazo_tshuma', N'Tshuma', N'', 0, 1, N'2026-04-08 09:08:28.780834', N'Mthandazo');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (238, N'pbkdf2_sha256$1000000$jVjvuB03MkUXaJGMpLmEhn$ILNSccwj84bjBuWu/S07Ew3WW+DJFMg2lvuidIhZxFs=', NULL, 0, N'sijabuliso_moyo', N'Moyo', N'', 0, 1, N'2026-04-08 09:08:29.559153', N'Sijabuliso');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (239, N'pbkdf2_sha256$1000000$WQM83MyY6P4Wj7yFYKZA7O$usk2GZFk9PcVlLCT/d9pAI9XUujPFhsq3aI14gvlYIc=', NULL, 0, N'linot_phiri', N'Phiri', N'', 0, 1, N'2026-04-08 09:08:30.377703', N'Linot');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (240, N'pbkdf2_sha256$1000000$F0fiRaD32taWTqF16XiPNK$z8tNnS/zdxtt8DRz5J30O2W/gjghMnO1/esXbpw0DvM=', NULL, 0, N'mhlengi_mathanda', N'Mathanda', N'', 0, 1, N'2026-04-08 09:08:31.228291', N'Mhlengi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (241, N'pbkdf2_sha256$1000000$xGPhGhcobVBrbg73apZ0PB$4Di0Jp1wpnMBd93mGXo+7ks8QP066gcUt9hoVwc1GeA=', NULL, 0, N'sineke_nyathi', N'Nyathi', N'', 0, 1, N'2026-04-08 09:08:32.237660', N'Sineke');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (242, N'pbkdf2_sha256$1000000$y0dsMcDyqxIecXKutusSLK$kveOBn1aLbwzAoOVSi6fx598BagnUF9wm8rQ5RpcbGo=', NULL, 0, N'shephered_ndlovu', N'Ndlovu', N'', 0, 1, N'2026-04-08 09:08:33.111422', N'Shephered');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (243, N'pbkdf2_sha256$1000000$tB8h8MoaF0pBJowoTp4KT4$+OHM4/p1iUwwoYTSFyE9V7OPS6ZhTJ7QaBllQoaMeCs=', NULL, 0, N'shelton_kwangware', N'Kwangware', N'', 0, 1, N'2026-04-08 09:08:33.861310', N'Shelton');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (244, N'pbkdf2_sha256$1000000$T1SApHKkm2f3kdisUNOVMW$3eZTfU3J2fVcfWY0cE08dpG5WBQ+lFsE/h2vJ+n9ZcM=', NULL, 0, N'philani_ndlovu', N'Ndlovu', N'', 0, 1, N'2026-04-08 09:08:34.659388', N'Philani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (245, N'pbkdf2_sha256$1000000$bOyGbeDxez1xIaivACLPdy$sLCDxzAgu1FH3WCZprJ0lCakLSB91bo3WSUlpCvKDaM=', NULL, 0, N'liberty_hwachi', N'Hwachi', N'', 0, 1, N'2026-04-08 09:08:35.487762', N'Liberty');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (246, N'pbkdf2_sha256$1000000$z1ynbJUYyjjNEXShijJrGJ$uQ45bjHyhS1BzsTV/0j8DjEHd5HGzceYxu/QJZ02qjI=', NULL, 0, N'obri_nkala', N'Nkala', N'', 0, 1, N'2026-04-08 09:08:36.281416', N'Obri');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (247, N'pbkdf2_sha256$1000000$aIOMZbyjQJknfl2RXiEL7N$8LdquG0EQ79tkUrI0E+Sav5D+PiT4ugIAOVECrTeQ+Q=', NULL, 0, N'alfred_tshuma', N'Tshuma', N'', 0, 1, N'2026-04-08 09:08:37.006179', N'Alfred');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (248, N'pbkdf2_sha256$1000000$0tPhhu0ZWi5v5XoNGbhZf1$R5AznNrhpeOZKOU8Dh33/aEF7hxtXfKK39Yv/3NYxfc=', NULL, 0, N'cleparton_ngwenya', N'Ngwenya', N'', 0, 1, N'2026-04-08 09:08:37.857428', N'Cleparton');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (249, N'pbkdf2_sha256$1000000$rVX0rEkLgcn26kWQvyAJwS$TrvmLef4I6Y7tj/R47978MPcBmV+7KY4EncsZR3adZU=', NULL, 0, N'privilege_msimanga', N'Msimanga', N'', 0, 1, N'2026-04-08 09:08:39.055627', N'Privilege');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (250, N'pbkdf2_sha256$1000000$RdV6X1XA295dbc9SPWyAtQ$RJAfHzuqbOd0/OI71QlAcmSDaGJ7cK9Mz9LQekpqHRE=', NULL, 0, N'brendon_makotore', N'Makotore', N'', 0, 1, N'2026-04-08 09:08:40.134489', N'Brendon');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (251, N'pbkdf2_sha256$1000000$nCyyJxvZ1L8vMHjKzuFCDY$91QCuqQXc0K3ESYlr7luLJor9JlbNvKlJRFSTQtF6Vs=', NULL, 0, N'noah_tiyanane', N'Tiyanane', N'', 0, 1, N'2026-04-08 09:08:41.143033', N'Noah');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (252, N'pbkdf2_sha256$1000000$MHBQYsbeGxD3xxg3EIBT7m$ugMHa7Z5FeXJmq9ySX9RyIgopp5H7k7rSVYo5Cm5Gc4=', NULL, 0, N'tarisayi_musiiwa', N'Musiiwa', N'', 0, 1, N'2026-04-08 09:08:42.287127', N'Tarisayi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (253, N'pbkdf2_sha256$1000000$e6wDuGN5Wz3zrh4iq2kiea$Ua3FBt2/IDdc85AgRZJugY8WA3+PjgOZ33/ufUTlxHw=', NULL, 0, N'dennis_chihlaro', N'Chihlaro', N'', 0, 1, N'2026-04-08 09:08:43.209329', N'Dennis');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (254, N'pbkdf2_sha256$1000000$g8BHYVm21205eZwx4zuC2V$wXZCnh8UkGebIJSmKtyWibkc/O23xZmI6bqe5txEwMU=', NULL, 0, N'thomas_chikandamoto', N'Chikandamoto', N'', 0, 1, N'2026-04-08 09:08:43.979865', N'Thomas');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (255, N'pbkdf2_sha256$1000000$LfROu7XtDpVfa1KHzx2Si0$Wpk3UVDx8aZXX3V5jSZSKgIKq+XeGH9oA6sX+RFJhe0=', NULL, 0, N'blessing_ganyani', N'Ganyani', N'', 0, 1, N'2026-04-08 09:08:44.712429', N'Blessing');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (256, N'pbkdf2_sha256$1000000$opDvoVByqsahNyc8gfUpth$ASAOi6AIL2rdD2zFLfRjbPXUsrxLbZbJxpfgdzzWC+k=', NULL, 0, N'christian_rafunya', N'Rafunya', N'', 0, 1, N'2026-04-08 09:08:45.528111', N'Christian');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (257, N'pbkdf2_sha256$1000000$upuTj7qn8pdux1YLKrY086$RybPTI1At0zcJJYqh8cOp3QslHkHIElQsl8BvD9ZgLI=', NULL, 0, N'tinotenda_sibanda', N'Sibanda', N'', 0, 1, N'2026-04-08 09:08:46.301400', N'Tinotenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (258, N'pbkdf2_sha256$1000000$BFFz5pee5YFKEz8Zuu61qq$lB2m+R124BO8HEioIXjsdLnJNMyMqD2No0ZTds2tVvk=', NULL, 0, N'nyasha_rukarwa', N'Rukarwa', N'', 0, 1, N'2026-04-08 09:08:47.236492', N'Nyasha');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (259, N'pbkdf2_sha256$1000000$GtQviJZyMi1xl9aWDP7EvT$slIqC24w3zDn1BXiNcnBchRrGA1mx7OTaMem7nmdILA=', NULL, 0, N'tafirekureva_muzeziwa', N'Muzeziwa', N'', 0, 1, N'2026-04-08 09:08:48.104283', N'Tafirekureva');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (260, N'pbkdf2_sha256$1000000$g7SdxXjxZMEgvBC7AzXf9e$ZTTn5LA7qc5myOLZnKTa4ieDfnu4bUCt/UzC0c5xM8g=', NULL, 0, N'william_sikhahlulo', N'Sikhahlulo', N'', 0, 1, N'2026-04-08 09:08:49.053694', N'William');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (261, N'pbkdf2_sha256$1000000$U4fgrI8WnggPfYjkUl716A$w0HhxnuhRtn1wRqBDYlASxfAOGRcZ3fwIgkEobHNRW0=', NULL, 0, N'paul_chikwenya', N'Chikwenya', N'', 0, 1, N'2026-04-08 09:08:49.956946', N'Paul');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (262, N'pbkdf2_sha256$1000000$uAKloimtZ8KnmeCjtJGf77$5PbD3lwtiYlQ8khSObyD+d8HSFuLvSAjQ1MKxSxmXQc=', NULL, 0, N'thulani_kanda', N'Kanda', N'', 0, 1, N'2026-04-08 09:08:50.937984', N'Thulani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (263, N'pbkdf2_sha256$1000000$YSXIeZumrxAYZYuGPK0kzF$bL7Jof4KWGC14gsSP90r5D7Mu1/vm9hr8hZiUX+RbBg=', NULL, 0, N'milton_manzungu', N'Manzungu', N'', 0, 1, N'2026-04-08 09:08:52.014437', N'Milton');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (264, N'pbkdf2_sha256$1000000$Y4rb4C1RgFiTfV9dRFidw9$FziLDYvqR0MckiFsC9bN1fYj1zg1pgW1T1auckb7EPo=', NULL, 0, N'mugove_chipunza', N'Chipunza', N'', 0, 1, N'2026-04-08 09:08:53.061322', N'Mugove');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (265, N'pbkdf2_sha256$1000000$niVA02vJFOhnkuDy0pShDt$1kP4VJDK/5o2+7k10bLlY/UwPNlCk2BcA+n5egv+j+A=', NULL, 0, N'hillary_bhulabhula', N'Bhulabhula', N'', 0, 1, N'2026-04-08 09:08:54.194299', N'Hillary');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (266, N'pbkdf2_sha256$1000000$ZcQzlT1fs9tUwVZgxiTLxQ$a6ec/H1FqSb0pkQllJoI8XRz14XZUXzzfTIohRtlFTY=', NULL, 0, N'clive_dube', N'Dube', N'', 0, 1, N'2026-04-08 09:08:55.266370', N'Clive');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (267, N'pbkdf2_sha256$1000000$4QZXfK0pTLl58Jw4WWE38c$WBEgrjfNkmhlcG0WnSU3kXWR87xXxQzvi64A1P29SMk=', NULL, 0, N'james_shoko', N'Shoko', N'', 0, 1, N'2026-04-08 09:08:56.451202', N'James');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (268, N'pbkdf2_sha256$1000000$lz4EsAEzNVqxqv5IV8Taab$6eweznnNsqtDnzBgbXF5lsLZCXXmYyoNTUmTOa0P+4Q=', NULL, 0, N'david_bore', N'Bore', N'', 0, 1, N'2026-04-08 09:08:57.480162', N'David');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (269, N'pbkdf2_sha256$1000000$EqX8M6C5tRNp5gGbdWwbeq$QyNBH7Yg+pI7kgvtTgEaFv8xrILenBfRtbGPErTsSys=', NULL, 0, N'tatenda_mandiopera', N'Mandiopera', N'', 0, 1, N'2026-04-08 09:08:58.423524', N'Tatenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (270, N'pbkdf2_sha256$1000000$xbSRHlsUFAfNFAfvyIe72i$jRsImqChLssJizNFOMwxQDfoM/RyV0+5CY9o7b/2Bmo=', NULL, 0, N'shepherd_mafa', N'Mafa', N'', 0, 1, N'2026-04-08 09:08:59.495968', N'Shepherd');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (271, N'pbkdf2_sha256$1000000$A5zuDizElO2v8JjLQ7WKyV$AjlgHZqW6OKeOEQNR+evaMDhJJs+MfUZjJ+l1MB406I=', NULL, 0, N'thomas_msapenda', N'Msapenda', N'', 0, 1, N'2026-04-08 09:09:00.663458', N'Thomas');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (272, N'pbkdf2_sha256$1000000$xdU80n9NOfdgqcbldoaajN$W5vPvrNORugi3Mn0wm+ff2dgKrzceidJzwBzZjKsxY4=', NULL, 0, N'stanselous_mudombo', N'Mudombo', N'', 0, 1, N'2026-04-08 09:09:01.573492', N'Stanselous');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (273, N'pbkdf2_sha256$1000000$VqnLa0ds5XD9kMZl8iwXed$q1GTRoFDcRXLCSrdyjcOEsv+9yF+edUJ9HW2AJVwyfU=', NULL, 0, N'felix_dhliwayo', N'Dhliwayo', N'', 0, 1, N'2026-04-08 09:09:02.475917', N'Felix');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (274, N'pbkdf2_sha256$1000000$T426lihZa9pi8SaFNGmOmv$HdrX5RsEu+nBnkYzIJ6SvIygB1Kd4ZR/atGJh2wGrP8=', NULL, 0, N'stalone_sisamala', N'Sisamala', N'', 0, 1, N'2026-04-08 09:09:03.247945', N'Stalone');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (275, N'pbkdf2_sha256$1000000$OngirynywO6hNeVJOQvPf9$szjy4rsIWLcBLw1VTLoYEUd3yrjHbQ9Dq3C4NLUec5g=', NULL, 0, N'tendai_misihairabwi', N'Misihairabwi', N'', 0, 1, N'2026-04-08 09:09:04.177782', N'Tendai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (276, N'pbkdf2_sha256$1000000$9Z3J6e042srNOuqyJzGWnQ$g+QDw8xZRjU8VYMbIIuLNjmC0LoeaBeA94fEHwaUl5A=', NULL, 0, N'kudakwashe_nyoni', N'Nyoni', N'', 0, 1, N'2026-04-08 09:09:05.165813', N'Kudakwashe');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (277, N'pbkdf2_sha256$1000000$TU5m84tiAU1TsgX8Op5xGS$GJfqtDS0gtcFbivW3FIXExJpRNWmqbCePeQbixjXbho=', NULL, 0, N'garikayi_musagwiza', N'Musagwiza', N'', 0, 1, N'2026-04-08 09:09:06.121601', N'Garikayi');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (278, N'pbkdf2_sha256$1000000$a13c72Lw8DAjuuITRXfumw$Oh2QYFXUSBQPpuxqAAIPxfdumBlioo7jH7RluofVWMU=', NULL, 0, N'rumbidzai_malamula', N'Malamula', N'', 0, 1, N'2026-04-08 09:09:07.130365', N'Rumbidzai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (279, N'pbkdf2_sha256$1000000$a7im8Cd8SWfEp3Rp0fTnx4$PbObM6MFFbAxBNoiuTKDkNhh8OOwFIokD5q5Akwnj/w=', NULL, 0, N'christmas_muchanga', N'Muchanga', N'', 0, 1, N'2026-04-08 09:09:07.928569', N'Christmas');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (280, N'pbkdf2_sha256$1000000$S1IHKgmjAdQyFSIm4KAVNv$r+XES3uK1W41BfciGdoXeXns8lVJnN68AHiC2g0zZGo=', NULL, 0, N'joseph_gurajena', N'Gurajena', N'', 0, 1, N'2026-04-08 09:09:08.768699', N'Joseph');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (281, N'pbkdf2_sha256$1000000$6cOwF8Rpx2Nux9pEBmov4P$lLbszpv6FAlaf0Qpze2D4oFqCuPULb0mrXJJM+U+z20=', NULL, 0, N'martin_makuwa', N'Makuwa', N'', 0, 1, N'2026-04-08 09:09:09.795194', N'Martin');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (282, N'pbkdf2_sha256$1000000$RxvqY3To5zWKwVyDOB88CQ$7RlsPWOOwGHPvyDRuGfQLfKvPjs2fQkBtoDsv3znty8=', NULL, 0, N'tinaye_chihwehwete', N'Chihwehwete', N'', 0, 1, N'2026-04-08 09:09:10.772060', N'Tinaye');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (283, N'pbkdf2_sha256$1000000$McJj9YGuQOwJhKgSzZ1iiq$EyiaPjGmvaBXTKIUhqrw81dDcN1+OIGLJ+8oTBHGEZU=', NULL, 0, N'kudzanai_manwa', N'Manwa', N'', 0, 1, N'2026-04-08 09:09:11.654601', N'Kudzanai');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (284, N'pbkdf2_sha256$1000000$vSRqVQTYyKyAjbs5SV5IMo$d/D59W2mawNUzxtSevvxSOdBSnJU4yMFpOyi9JLifYs=', NULL, 0, N'leonard_mhangami', N'Mhangami', N'', 0, 1, N'2026-04-08 09:09:12.448787', N'Leonard');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (285, N'pbkdf2_sha256$1000000$aZ6YuXbC4UkUS1M8IGPVDo$4ymmexe7XzmdF90q0QjfVVRBYA5zbZLle6l/xD9CTeY=', NULL, 0, N'ozias_gondo', N'Gondo', N'', 0, 1, N'2026-04-08 09:09:13.323183', N'Ozias');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (286, N'pbkdf2_sha256$1000000$uUgO0HyohhfSJsOTlaY9T3$5ZX9D+ajVt+7C/s2G47tRh5Yf+tsgdrqw6RPZAsWxsc=', NULL, 0, N'murphree_wadzingenyama', N'Wadzingenyama', N'', 0, 1, N'2026-04-08 09:09:14.299505', N'Murphree');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (287, N'pbkdf2_sha256$1000000$dbAEhkw9zQx6C8sk5P3JLm$upW8r9hytAgLs5MSj8NJZq+aw3bJw5oZtV634Yv7BV8=', NULL, 0, N'stanley_matare', N'Matare', N'', 0, 1, N'2026-04-08 09:09:15.193294', N'Stanley');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (288, N'pbkdf2_sha256$1000000$w8qShvP8QXTWqgqGusSka1$kYptTqXXhpmLkCZMxS1+nSgjQUrkb6ktUrhYDVH44x8=', NULL, 0, N'tatenda_jesa', N'Jesa', N'', 0, 1, N'2026-04-08 09:09:16.115087', N'Tatenda');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (289, N'pbkdf2_sha256$1000000$XGa0u4jjjep723qU0uPD4o$/TX3FUglBHpIqUvxuiQlGHtJ3xb2mlE97gKkio6YcJ0=', NULL, 0, N'ephias_musariri', N'Musariri', N'', 0, 1, N'2026-04-08 09:09:17.012744', N'Ephias');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (290, N'pbkdf2_sha256$1000000$8TqE5GCoEpux8Eyz4DwFxz$fz30hEmgxht1R+0J9CExTajPWOs7pIgSuIV8/bodxUQ=', NULL, 0, N'ishamael_mavhinga', N'Mavhinga', N'', 0, 1, N'2026-04-08 14:07:13.472984', N'Ishamael');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (291, N'pbkdf2_sha256$1200000$djmdYMCXBe1c7QzxeRPi58$QU88o5qMxool3WfBETZKxsQULLO2WKT5rLSjrZxnymE=', N'2026-04-08 17:34:25.707661', 0, N'method_sibanda', N'Sibanda', N'', 0, 1, N'2026-04-08 14:07:13.929777', N'Method');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (292, N'pbkdf2_sha256$1000000$xaqR0PvnWAzsdHk4o3WeKS$byYUpu45IrnmSZfVfTfVao92o5abgkmF17KUCAqd1+4=', NULL, 0, N'clayton_maponga', N'Maponga', N'', 0, 1, N'2026-04-08 14:07:14.357456', N'Clayton');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (293, N'pbkdf2_sha256$1000000$crO0DPKOBIdLUKzN1KUGLm$xlDgAWC7Q+uT/3lKnJcuSzmipXpLn/wB7l9yirxLhJ8=', NULL, 0, N'libangani_chdhakwa', N'Chdhakwa', N'', 0, 1, N'2026-04-08 14:07:14.782089', N'Libangani');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (294, N'pbkdf2_sha256$1000000$anU1hazwvbDG9y9z4bcsqt$Y1qC1qoN7rDiU/lKEwK+P7wS5eGs3zqxA/dLJWHcfEQ=', NULL, 0, N'arnold_tsande', N'Tsande', N'', 0, 1, N'2026-04-08 14:07:15.220098', N'Arnold');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (295, N'pbkdf2_sha256$1000000$o9VFVxH4Gus6M4fBJJMElh$29vDS9tURqLVPGnAKPXhwGKM8UuO3YessdAl/oCbSUk=', NULL, 0, N'nicodemus_bere', N'Bere', N'', 0, 1, N'2026-04-08 14:07:15.784992', N'Nicodemus');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (296, N'pbkdf2_sha256$1000000$gipUkohz5AH4VlaJi9JDT1$2ZRv8dhO99KkK2v6C3XOHgVOmjqzEJp65tVFqqOZMRo=', NULL, 0, N'tapiwa_madziwire', N'Madziwire', N'', 0, 1, N'2026-04-08 14:07:16.229382', N'Tapiwa');
INSERT INTO dbo.[auth_user] ([id], [password], [last_login], [is_superuser], [username], [last_name], [email], [is_staff], [is_active], [date_joined], [first_name]) VALUES (297, N'pbkdf2_sha256$1000000$uGqsPxTliriMH7UqqMpI02$mva51G+6Eb00I6Cwou+k5EVpsMvpfW4FJAIjdmug7yA=', NULL, 0, N'richard_shumbairerwa', N'Shumbairerwa', N'', 0, 1, N'2026-04-08 14:07:16.667930', N'Richard');

-- django_content_type
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (1, N'admin', N'logentry');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (2, N'auth', N'permission');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (3, N'auth', N'group');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (4, N'auth', N'user');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (5, N'contenttypes', N'contenttype');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (6, N'sessions', N'session');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (7, N'operations', N'bike');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (8, N'operations', N'district');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (9, N'operations', N'province');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (10, N'operations', N'facility');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (11, N'operations', N'pcprofile');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (12, N'operations', N'riderprofile');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (13, N'operations', N'riderweeklyreport');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (14, N'operations', N'reporteditsnapshot');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (15, N'operations', N'reportauditlog');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (16, N'operations', N'userprofile');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (17, N'operations', N'registereddevice');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (18, N'operations', N'ridertripentry');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (19, N'operations', N'samplerejection');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (20, N'operations', N'car');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (21, N'operations', N'referredsample');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (22, N'operations', N'pcdistrictweeklytransportstat');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (23, N'operations', N'lab');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (24, N'operations', N'riderremoteconfig');
INSERT INTO dbo.[django_content_type] ([id], [app_label], [model]) VALUES (25, N'operations', N'riderdevice');

-- django_session
INSERT INTO dbo.[django_session] ([session_key], [session_data], [expire_date]) VALUES (N'rni7umonke7ab17c44gugk6kixciz75n', N'.eJxVjEEOwiAQRe_C2hCgdMi4dO8ZCMNMpWogKe3KeHdt0oVu_3vvv1RM21ri1mWJM6uzsur0u1HKD6k74Huqt6Zzq-syk94VfdCur43leTncv4OSevnWBMYHYMnEzGjBIshEIYwwGAAUGK0nHLLzYDiTEXYGh0kIvRMUo94f5VI33w:1wAMwp:DTre3xsnvzR_Jg-c5IOJDGxtAVXBkYHIHTmOiS-9tC8', N'2026-04-22 07:03:35.394978');
INSERT INTO dbo.[django_session] ([session_key], [session_data], [expire_date]) VALUES (N'h44er5ifhj507ngjkj8pbnwmma63fo28', N'.eJxVjEEOwiAQRe_C2hAYwYJL9z0DGYZBqgaS0q6Md7dNutDtf-_9twi4LiWsnecwJXEVZ3H63SLSk-sO0gPrvUlqdZmnKHdFHrTLsSV-3Q7376BgL1ttHDuvyGjvQIG-5ITZO8cUreJkGCArsibrgVEjqLhJVpsBiIyPhOLzBdX6N78:1wAWwa:1JzpAhks3h5IO_-xehCLyNtTeoMSTJjgMswauk89_M8', N'2026-04-22 17:44:00.065906');

-- operations_bike
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (1, N'AER6999', N'', 1, 1, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (2, N'AER4409', N'', 1, 1, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (3, N'AAY8044', N'', 1, 1, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (4, N'AER4045', N'', 1, 2, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (5, N'GHCC3347', N'', 1, 3, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (6, N'AER0852', N'', 1, 3, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (7, N'AAE9964', N'', 1, 3, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (8, N'AER3190', N'', 1, 3, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (9, N'ACD9979', N'', 1, 4, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (10, N'GHCW1429', N'', 1, 4, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (11, N'GHCC1596', N'', 1, 4, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (12, N'GHCC3344', N'', 1, 5, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (13, N'AER4417', N'', 1, 5, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (14, N'AGR9421', N'', 1, 5, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (15, N'GHCC3309', N'', 1, 5, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (16, N'AER4213', N'', 1, 5, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (17, N'GHCC3315', N'', 1, 5, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (18, N'GHCC3051', N'', 1, 6, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (19, N'GHCC3076', N'', 1, 6, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (20, N'GHCC3028', N'', 1, 6, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (21, N'GHCC3042', N'', 1, 6, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (22, N'AER0905', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (23, N'GHCC3316', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (24, N'AER4234', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (25, N'GHCC3073', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (26, N'AGR9423', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (27, N'AER3626', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (28, N'GHCC3319', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (29, N'GHCC3320', N'', 1, 7, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (30, N'AER5529', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (31, N'AER3520', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (32, N'AER5517', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (33, N'AER6933', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (34, N'GHCC3103', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (35, N'GHCC3312', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (36, N'GHCC3318', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (37, N'GHCC3332', N'', 1, 8, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (38, N'AER4214', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (39, N'AER0908', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (40, N'AER4044', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (41, N'AER5533', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (42, N'GHCC3112', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (43, N'GHCC3313', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (44, N'GHCC3322', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (45, N'GHCC3336', N'', 1, 9, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (46, N'GHCC3314', N'', 1, 10, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (47, N'GHCC3113', N'', 1, 10, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (48, N'AER4212', N'', 1, 10, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (49, N'AER7020', N'', 1, 10, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (50, N'AER1429', N'', 1, 10, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (51, N'AER4351', N'', 1, 10, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (52, N'GHCC3018', N'', 1, 11, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (53, N'GHCC3091', N'', 1, 11, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (54, N'GHCC3003', N'', 1, 11, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (55, N'GHCC3017', N'', 1, 11, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (56, N'GHCC3034', N'', 1, 11, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (57, N'AER4375', N'', 1, 12, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (58, N'AGR9891', N'', 1, 12, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (59, N'AER7005', N'', 1, 12, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (60, N'AER7207', N'', 1, 12, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (61, N'GHCC3110', N'', 1, 12, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (62, N'AER5521', N'', 1, 13, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (63, N'AER4377', N'', 1, 13, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (64, N'AER7019', N'', 1, 13, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (65, N'AER4238', N'', 1, 13, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (66, N'AER7001', N'', 1, 14, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (67, N'AER4043', N'', 1, 14, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (68, N'GHCC3310', N'', 1, 14, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (69, N'AER5530', N'', 1, 14, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (70, N'GHCC3039', N'', 1, 15, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (71, N'GHCC3046', N'', 1, 15, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (72, N'GHCC3040', N'', 1, 15, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (73, N'GHCC3048', N'', 1, 15, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (74, N'GHCC3016', N'', 1, 16, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (75, N'GHCC3009', N'', 1, 16, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (76, N'GHCC3015', N'', 1, 16, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (77, N'GHCC3019', N'', 1, 17, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (78, N'GHCC3022', N'', 1, 17, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (79, N'GHCC3024', N'', 1, 17, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (80, N'GHCC3043', N'', 1, 18, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (81, N'GHCC3054', N'', 1, 18, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (82, N'GHCC3057', N'', 1, 18, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (83, N'GHCC3029', N'', 1, 19, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (84, N'GHCC3030', N'', 1, 19, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (85, N'GHCC3037', N'', 1, 19, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (86, N'GHCC2999', N'', 1, 20, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (87, N'GHCC3038', N'', 1, 20, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (88, N'GHCC3311', N'', 1, 20, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (89, N'GHCC3059', N'', 1, 20, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (90, N'GHCC3093', N'', 1, 20, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (91, N'GHCC3011', N'', 1, 20, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (92, N'GHCC3080', N'', 1, 21, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (93, N'GHCC3082', N'', 1, 21, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (94, N'GHCC3088', N'', 1, 21, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (95, N'GHCC3064', N'', 1, 22, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (96, N'GHCC3075', N'', 1, 22, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (97, N'GHCC3066', N'', 1, 22, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (98, N'GHCC3063', N'', 1, 22, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (99, N'GHCC3067', N'', 1, 22, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (100, N'GHCC3062', N'', 1, 23, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (101, N'GHCC3087', N'', 1, 23, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (102, N'GHCC3065', N'', 1, 23, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (103, N'GHCC3079', N'', 1, 24, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (104, N'GHCC3083', N'', 1, 24, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (105, N'GHCC3092', N'', 1, 24, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (106, N'GHCC3052', N'', 1, 25, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (107, N'GHCC3058', N'', 1, 25, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (108, N'GHCC3050', N'', 1, 25, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (109, N'AER3119', N'', 1, 26, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (110, N'GHCC3111', N'', 1, 26, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (111, N'AGR9349', N'', 1, 26, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (112, N'AER7015', N'', 1, 27, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (113, N'AER5524', N'', 1, 27, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (114, N'AER4353', N'', 1, 27, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (115, N'AER4244', N'', 1, 27, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (116, N'GHCW1001', N'', 1, 28, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (117, N'GHCC3339', N'', 1, 28, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (118, N'AER4046', N'', 1, 28, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (119, N'AGR9490', N'', 1, 28, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (120, N'GHCC3049', N'', 1, 25, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (121, N'AER7011', N'', 1, 26, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (122, N'GHCC3060', N'', 1, 23, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (123, N'GHCC3069', N'', 1, 23, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (124, N'GHCC3118', N'', 1, 29, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (125, N'AER1430', N'', 1, 29, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (126, N'GHCC3119', N'', 1, 29, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (127, N'GHCC3343', N'', 1, 29, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (128, N'AER4233', N'', 1, 29, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (129, N'AER7009', N'', 1, 29, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (130, N'AER4378', N'', 1, 30, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (131, N'AER4218', N'', 1, 30, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (132, N'GHCC3327', N'', 1, 30, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (133, N'GHCC3348', N'', 1, 30, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (134, N'AER7012', N'', 1, 30, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (135, N'GHCC3102', N'', 1, 30, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (136, N'GHCC3115', N'', 1, 31, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (137, N'AER4217', N'', 1, 31, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (138, N'GHCC3317', N'', 1, 31, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (139, N'AER7021', N'', 1, 31, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (140, N'AER7206', N'', 1, 31, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (141, N'GHCC2996', N'', 1, 32, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (142, N'GHCC3000', N'', 1, 32, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (143, N'GHCC3013', N'', 1, 32, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (144, N'GHCC3090', N'', 1, 33, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (145, N'GHCC3032', N'', 1, 33, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (146, N'GHCC3044', N'', 1, 33, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (147, N'GHCC3047', N'', 1, 33, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (148, N'GHCC3100', N'', 1, 34, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (149, N'GHCC3056', N'', 1, 34, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (150, N'AER4229', N'', 1, 34, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (151, N'AER7013', N'', 1, 34, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (152, N'GHCC3326', N'', 1, 34, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (153, N'AGR9491', N'', 1, 34, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (154, N'AER7014', N'', 1, 35, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (155, N'AER4358', N'', 1, 35, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (156, N'AER4230', N'', 1, 35, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (157, N'GHCC3323', N'', 1, 35, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (158, N'GHCC3096', N'', 1, 36, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (159, N'GHCC3308', N'', 1, 37, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (160, N'AER2200', N'', 1, 37, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (161, N'GHCC3328', N'', 1, 37, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (162, N'AER4053', N'', 1, 37, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (163, N'AER4056', N'', 1, 38, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (164, N'AER4052', N'', 1, 38, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (165, N'AER4360', N'', 1, 38, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (166, N'AER4456', N'', 1, 38, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (167, N'GHCC3104', N'', 1, 38, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (168, N'GHCC3349', N'', 1, 38, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (169, N'AER4051', N'', 1, 39, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (170, N'AGR9783', N'', 1, 39, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (171, N'AER7208', N'', 1, 40, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (172, N'AER7003', N'', 1, 40, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (173, N'AER4049', N'', 1, 40, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (174, N'GHCC3321', N'', 1, 40, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (175, N'GHCC3335', N'', 1, 39, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (176, N'AER4359', N'', 1, 39, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (177, N'GHCC3068', N'', 1, 41, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (178, N'GHCC3045', N'', 1, 41, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (179, N'GHCC3070', N'', 1, 41, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (180, N'GHCC3085', N'', 1, 41, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (181, N'GHCC3094', N'', 1, 41, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (182, N'ADO4784', N'', 1, 42, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (183, N'AER4215', N'', 1, 42, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (184, N'GHCC3095', N'', 1, 42, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (185, N'GHCC3346', N'', 1, 42, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (186, N'AER4050', N'', 1, 42, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (187, N'GHCC3072', N'', 1, 42, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (188, N'ADO4385', N'', 1, 36, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (189, N'AER4055', N'', 1, 36, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (190, N'AER4210', N'', 1, 43, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (191, N'AER7006', N'', 1, 43, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (192, N'GHCC3116', N'', 1, 43, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (193, N'GHCC3004', N'', 1, 44, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (194, N'GHCC3055', N'', 1, 44, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (195, N'GHC3084', N'', 1, 44, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (196, N'ACA2469', N'', 1, 45, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (197, N'AER4211', N'', 1, 45, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (198, N'GHCC3031', N'', 1, 46, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (199, N'GHCC3002', N'', 1, 46, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (200, N'GHCC3074', N'', 1, 46, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (201, N'GHCC3061', N'', 1, 46, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (202, N'GHCC3026', N'', 1, 46, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (203, N'GHCC3008', N'', 1, 46, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (204, N'AGR9294', N'', 1, 47, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (205, N'GHCC3333', N'', 1, 47, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (206, N'AER4208', N'', 1, 47, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (207, N'AER3074', N'', 1, 48, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (208, N'AER4066', N'', 1, 48, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (209, N'AER4380', N'', 1, 48, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (210, N'AER7073', N'', 1, 48, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (211, N'AER4048', N'', 1, 49, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (212, N'AER7071', N'', 1, 49, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (213, N'AER1295', N'', 1, 49, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (214, N'AGR9890', N'', 1, 49, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (215, N'ACA2470', N'', 1, 43, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (216, N'AER4361', N'', 1, 50, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (217, N'AGR9350', N'', 1, 50, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (218, N'GHCC3005', N'', 1, 50, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (219, N'AER7010', N'', 1, 51, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (220, N'AER4059', N'', 1, 51, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (221, N'AER4064', N'', 1, 51, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (222, N'GHCC3071', N'', 1, 51, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (223, N'AER7000', N'', 1, 52, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (224, N'AER3512', N'', 1, 52, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (225, N'AGR9724', N'', 1, 52, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (226, N'GHCC3341', N'', 1, 52, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (227, N'AER4381', N'', 1, 53, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (228, N'AER4063', N'', 1, 53, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (229, N'AER4065', N'', 1, 53, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (230, N'GHCC3342', N'', 1, 53, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (231, N'AER4061', N'', 1, 54, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (232, N'GHCC3105', N'', 1, 54, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (233, N'GHCC3324', N'', 1, 54, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (234, N'AER1291', N'', 1, 55, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (235, N'AER4060', N'', 1, 55, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (236, N'GHCC3117', N'', 1, 55, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (237, N'GHCC3340', N'', 1, 55, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (238, N'GHCC3089', N'', 1, 56, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (239, N'GHCC3041', N'', 1, 56, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (240, N'GHCC3001', N'', 1, 56, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (241, N'AER3176', N'', 1, 57, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (242, N'AER5512', N'', 1, 57, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (243, N'AER5522', N'', 1, 57, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (244, N'ADO9585', N'', 1, 58, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (245, N'AER4057', N'', 1, 58, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (246, N'GHCC3107', N'', 1, 58, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (247, N'AER4047', N'', 1, 58, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (248, N'AER7017', N'', 1, 59, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (249, N'GHCC3329', N'', 1, 59, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (250, N'AER4058', N'', 1, 59, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (251, N'AER0880', N'', 1, 59, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (252, N'GHCC3101', N'', 1, 59, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (253, N'AER4239', N'', 1, 59, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (254, N'AGR9424', N'', 1, 60, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (255, N'GHCC3325', N'', 1, 60, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (256, N'GHCC3330', N'', 1, 60, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (257, N'AER4054', N'', 1, 60, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (258, N'GHCC3109', N'', 1, 60, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (259, N'GHCC3081', N'', 1, 61, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (260, N'GHCC2997', N'', 1, 61, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (261, N'GHCC3012', N'', 1, 62, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (262, N'GHCC3021', N'', 1, 62, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (263, N'GHCC2998', N'', 1, 62, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (264, N'GHCC3006', N'', 1, 62, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (265, N'GHCC3033', N'', 1, 63, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (266, N'GHCC3077', N'', 1, 63, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (267, N'GHCC3078', N'', 1, 63, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (268, N'GHCC3053', N'', 1, 63, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (269, N'GHCC3027', N'', 1, 63, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (270, N'GHCC3020', N'', 1, 64, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (271, N'GHCC3036', N'', 1, 64, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (272, N'GHCC3007', N'', 1, 64, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (273, N'GHCC3023', N'', 1, 64, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (274, N'GHCC3025', N'', 1, 64, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (275, N'GHCC3086', N'', 1, 61, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (276, N'GHCC3035', N'', 1, 61, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (277, N'GHCC3345', N'', 1, 57, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (278, N'AER4042', N'', 1, 57, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (279, N'AER5515', N'', 1, 57, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (280, N'GHCC3106', N'', 1, 60, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (281, N'GHCC3159', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (282, N'GHCC3161', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (283, N'GHCC3158', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (284, N'GHCC3163', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (285, N'GHCC3157', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (286, N'GHCC3164', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (287, N'GHCC3162', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');
INSERT INTO dbo.[operations_bike] ([id], [code], [notes], [active], [district_id], [snp_bike_accident], [snp_bike_breakdown], [snp_bike_no_fuel], [snp_bike_routine_service], [snp_clinical_ip], [snp_inclement_weather], [snp_other], [snp_other_specify], [snp_rider_annual_leave], [snp_rider_sick_leave], [mitigation_measures]) VALUES (288, N'GHCC3160', N'', 1, NULL, 0, 0, 0, 0, 0, 0, 0, N'', 0, 0, N'');

-- operations_car
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (1, N'GHCC3159', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (2, N'GHCC3161', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (3, N'GHCC3158', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (4, N'GHCC3163', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (5, N'GHCC3157', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (6, N'GHCC3164', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (7, N'GHCC3162', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);
INSERT INTO dbo.[operations_car] ([id], [code], [notes], [active], [snp_bike_breakdown], [snp_bike_routine_service], [snp_bike_no_fuel], [snp_rider_sick_leave], [snp_rider_annual_leave], [snp_inclement_weather], [snp_bike_accident], [snp_clinical_ip], [snp_other], [snp_other_specify], [mitigation_measures], [district_id]) VALUES (8, N'GHCC3160', N'', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, N'', N'', NULL);

-- operations_district
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (1, N'Bulawayo', 3, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (2, N'City of Bulawayo', 3, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (3, N'Harare', 6, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (4, N'Harare City', 6, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (5, N'Buhera', 4, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (6, N'Chimanimani', 4, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (7, N'Chipinge', 4, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (8, N'Makoni', 4, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (9, N'Mutare', 4, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (10, N'Mutasa', 4, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (11, N'Nyanga', 4, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (12, N'Mount Darwin', 1, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (13, N'Guruve', 1, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (14, N'Mazowe', 1, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (15, N'Bindura', 1, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (16, N'Shamva', 1, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (17, N'Rushinga', 1, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (18, N'Centenary', 1, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (19, N'Mbire', 1, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (20, N'Chikomba', 5, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (21, N'Hwedza', 5, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (22, N'Mudzi', 5, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (23, N'Mutoko', 5, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (24, N'Seke', 5, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (25, N'UMP', 5, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (26, N'Murewa', 5, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (27, N'Marondera', 5, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (28, N'Goromonzi', 5, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (29, N'Zvimba', 10, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (30, N'Makonde', 10, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (31, N'Kadoma Sanyati', 10, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (32, N'Kariba', 10, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (33, N'Mhondoro', 10, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (34, N'Hurungwe', 10, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (35, N'Chegutu', 10, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (36, N'Chivi', 9, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (37, N'Gutu', 9, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (38, N'Masvingo', 9, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (39, N'Mwenezi', 9, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (40, N'Zaka', 9, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (41, N'Bikita', 9, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (42, N'Chiredzi', 9, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (43, N'Umguza', 2, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (44, N'Binga', 2, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (45, N'Bubi', 2, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (46, N'Hwange', 2, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (47, N'Lupane', 2, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (48, N'Nkayi', 2, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (49, N'Tsholotsho', 2, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (50, N'Bulilima', 8, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (51, N'Beitbridge', 8, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (52, N'Gwanda', 8, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (53, N'Insiza', 8, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (54, N'Matobo', 8, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (55, N'Umzingwane', 8, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (56, N'Mangwe', 8, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (57, N'Gokwe South', 7, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (58, N'Gweru', 7, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (59, N'Kwekwe', 7, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (60, N'Mberengwa', 7, N'DSD');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (61, N'Chirumhanzu', 7, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (62, N'Zvishavane', 7, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (63, N'Shurugwi', 7, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (64, N'Gokwe North', 7, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (65, N'Uzumba Maramba Pfungwe', 5, N'TA-SDI');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (66, N'Mt. Darwin', 1, N'');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (67, N'Murehwa', 5, N'');
INSERT INTO dbo.[operations_district] ([id], [name], [province_id], [support_type]) VALUES (68, N'Kadoma', 10, N'');

-- operations_facility
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1, N'Biriwiri Rural Hospital', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (2, N'Bumba Rural Health Centre', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (3, N'Chakohwa Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (4, N'Changazi Rural Health Centre', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (5, N'Charter Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (6, N'Chayamiti Rural Health Centre', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (7, N'Chikukwa Rural Health Centre', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (8, N'Chikwakwa Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (9, N'Chimanimani Rural Hospital', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (10, N'Chimanimani Urban Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (11, N'Chisengu Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (12, N'Gudyanga Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (13, N'Muchadziya Rural Health Centre', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (14, N'Mutambara Mission Hospital', N'hub', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (15, N'Mutsvangwa Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (16, N'Ngorima Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (17, N'Nhedziwa Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (18, N'Nyabamba Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (19, N'Nyahode Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (20, N'Nyanyadzi Rural Hospital', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (21, N'Roscommon Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (22, N'Rusitu Mission Hospital', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (23, N'Shinja Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (24, N'Tilbury Clinic', N'clinic', 6, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (25, N'Avilla Mission Hospital', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (26, N'Bende Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (27, N'Chatindo Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (28, N'Chiwarira Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (29, N'Claremont Estate Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (30, N'Dombo Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (31, N'Elim Mission Hospital', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (32, N'Erin Forest Estate Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (33, N'Fombe Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (34, N'Gairezi Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (35, N'Gotekote Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (36, N'Kambudzi Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (37, N'Matize Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (38, N'Mount Melleray Mission Hospital', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (39, N'Nyadowa Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (40, N'Nyafaru Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (41, N'Nyajezi Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (42, N'Nyamaropa Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (43, N'Nyamombe Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (44, N'Nyanga District Hospital', N'hub', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (45, N'Nyarumvurwe Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (46, N'Nyatate Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (47, N'Nyautare Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (48, N'Regina Coeli Mission Hospital', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (49, N'Ruchera Rural Health Centre', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (50, N'Sabvure Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (51, N'Spring Valley Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (52, N'Tombo Clinic', N'clinic', 11, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (53, N'Always - 100007 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (54, N'Chadereka - 100123 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (55, N'Chawarura - 100147 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (56, N'Chidikamwedzi - 100171 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (57, N'Chinyani - 100241 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (58, N'Chiwenga Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (59, N'Dambakurima - 100359 - Rural Health Centre', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (60, N'David Nelson - 100372 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (61, N'Hoya - 100612 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (62, N'Hwata - 100624 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (63, N'Machaya - 100798 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (64, N'Muzarabani - 101189 - Clinic', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (65, N'St. Albert''s - 101623 - Mission Hospital', N'clinic', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (66, N'Bindura Farm Health Scheme Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (67, N'Bindura Provincial Hospital', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (68, N'Chipadze Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (69, N'Chiriseri Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (70, N'Chiveso Rural Health Centre', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (71, N'Chiwaridzo Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (72, N'Foothills Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (73, N'Freda Rebecca Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (74, N'Glamorgan Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (75, N'Katanya Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (76, N'Manga Rural Health Centre', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (77, N'Manhenga Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (78, N'Muonwe Rural Health Centre', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (79, N'Mupandira Rural Health Centre', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (80, N'Nyava Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (81, N'Rusununguko Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (82, N'Rutope Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (83, N'Takunda Rural Health Centre', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (84, N'Trojan Nickel Clinic', N'clinic', 15, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (85, N'Angwa Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (86, N'Chapoto Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (87, N'Chidodo Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (88, N'Chikafa Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (89, N'Chirunya Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (90, N'Chitsungo Mission Hospital', N'hub', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (91, N'Gonono Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (92, N'Mahuwe Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (93, N'Masoka Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (94, N'Masomo Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (95, N'Musengezi Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (96, N'Mushumbi RHC', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (97, N'Nyambudzi Clinic', N'clinic', 19, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (98, N'Bungwe Clinic', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (99, N'Chimandau Rural Health Centre', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (100, N'Chimhanda Clinic', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (101, N'Chimhanda District Hospital', N'hub', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (102, N'Ganganyama Clinic', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (103, N'Mary Mount Mission Hospital', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (104, N'Mazowe Bridge Rural Health Centre', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (105, N'Mukonde Rural Health Centre', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (106, N'Mukosa Rural Health Centre', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (107, N'Nhawa Rural Health Centre', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (108, N'Nyamatikiti Rural Health Centre', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (109, N'Rusambo Clinic', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (110, N'Rushinga Rural Health Centre', N'clinic', 17, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (111, N'Bushu Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (112, N'Chidembo Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (113, N'Chihuri Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (114, N'Chipoli Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (115, N'Chishapa Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (116, N'Goora Rural Health Centre', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (117, N'Madziwa Rural Hospital', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (118, N'Madziwa Teachers'' College', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (119, N'Mliti clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (120, N'Mupfurudzi Rural Health Centre', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (121, N'Nyamaropa Rural Health Centre', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (122, N'Nyamaruro Rural Health Centre', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (123, N'Shamva District Hospital', N'hub', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (124, N'Shamva Gold Mine Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (125, N'Takawira Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (126, N'Wadzanai Clinic', N'clinic', 16, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (127, N'Bvumbura Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (128, N'Chivhu Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (129, N'Chivhu General Hospital', N'hub', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (130, N'Daramombe Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (131, N'Gandachibvuva Mission Hospital', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (132, N'Gandami Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (133, N'Gokomere Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (134, N'Lancashire Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (135, N'Madamombe Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (136, N'Manyene Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (137, N'Masasa Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (138, N'Mbiru Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (139, N'Mufudziwakanaka Rural Health Centre', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (140, N'Murezi Rural Health Centre', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (141, N'Mushipe Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (142, N'Musumha Rural Health Centre', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (143, N'Mutoro Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (144, N'Mwerahari Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (145, N'Nhangabwe Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (146, N'Nharira Rural Hospital', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (147, N'Nyamhere Rural Health Centre', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (148, N'Philipsdale Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (149, N'Pokoteke Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (150, N'Range Rural Health Centre', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (151, N'Rutanhira Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (152, N'Sadza District Hospital', N'hub', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (153, N'Shumba Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (154, N'Tavara Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (155, N'Unyetu Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (156, N'Wazvaramhaka Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (157, N'Wiltshire Clinic', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (158, N'Zvamatobwe Rural Health Centre', N'clinic', 20, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (159, N'Chigondo Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (160, N'Chikurumadziva Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (161, N'Chirume Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (162, N'Garaba Rural Health Centre', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (163, N'Goneso Rural Health Centre', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (164, N'Goto Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (165, N'Gotora/Skimpton Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (166, N'Hwedza Rural Hospital', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (167, N'Idube Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (168, N'Makarara Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (169, N'Mt St Mary''s Mission Hospital', N'hub', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (170, N'Mukamba Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (171, N'Sango Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (172, N'Sengezi Rural Health Centre', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (173, N'Zviduri Clinic', N'clinic', 21, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (174, N'Chikwizo Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (175, N'Chimukoko Rural Health Centre', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (176, N'Chingamuka Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (177, N'Chisvo Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (178, N'Chiunye Rural Health Centre', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (179, N'Dendera Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (180, N'Goromonzi Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (181, N'Gozi Rural Health Centre', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (182, N'Kapotesa Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (183, N'Kondo Rural Health Centre', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (184, N'Kotwa Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (185, N'Kotwa District Hospital', N'hub', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (186, N'Makaha Rural Health Centre', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (187, N'Masarakufa Rural Health Centre', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (188, N'Masenda Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (189, N'Mavhurazi clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (190, N'Nyahuku Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (191, N'Nyamande Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (192, N'Nyamanyora Rural Health Centre', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (193, N'Nyamapanda Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (194, N'Nyamatawa Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (195, N'Nyamukoho Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (196, N'Nyapfunde Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (197, N'Nyarutepo Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (198, N'Shinga Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (199, N'St Pius Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (200, N'Suswe Clinic', N'clinic', 22, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (201, N'Charehwa Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (202, N'Chidye Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (203, N'Chikondoma Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (204, N'Chindenga Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (205, N'Hoyuyu I Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (206, N'Hoyuyu II Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (207, N'Kapondoro Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (208, N'Katsukunya Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (209, N'Kawazva Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (210, N'Kawere Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (211, N'Kowo Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (212, N'Kushinga Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (213, N'Luisa Guidotti Mission Hospital', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (214, N'Madimutsa Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (215, N'Makosa Rural Hospital', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (216, N'Matedza Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (217, N'Mother of Peace Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (218, N'Mushimbo Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (219, N'Mutemwa Leprosy Settlement Clinic', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (220, N'Mutoko District Hospital', N'hub', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (221, N'Nyadire Mission Hospital', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (222, N'Nyadire Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (223, N'Nyamuzizi Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (224, N'Nyamuzuwe Rural Hospital', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (225, N'Nzira Rural Health Centre', N'clinic', 23, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (226, N'Acton Reynolds Rural Health Centre', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (227, N'Beatrice Rural Hospital', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (228, N'Charakupa Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (229, N'Epworth Mission Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (230, N'Epworth Polyclinic', N'hub', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (231, N'Jonasi Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (232, N'Kunaka Hospital', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (233, N'Lanark Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (234, N'Makanyazingwa Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (235, N'Marirangwe Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (236, N'Masasa Rural Health Centre', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (237, N'Muda Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (238, N'Overspill Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (239, N'Ringa Rural Health Centre', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (240, N'Wheelerdale Clinic', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (241, N'Zhakata Rural Health Centre', N'clinic', 24, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (242, N'Borera Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (243, N'Chikuhwa Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (244, N'Chipfunde Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (245, N'Chitimbe Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (246, N'Chitsungo Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (247, N'Dewe Council Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (248, N'Dindi Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (249, N'Hombiro Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (250, N'Kafura Rural Health Centre', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (251, N'Karimbika Rural Health Centre', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (252, N'Manyika Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (253, N'Maramba Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (254, N'Marembera Rural Health Centre', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (255, N'Mashambanhaka Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (256, N'Muskwe Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (257, N'Mutawatawa District Hospital', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (258, N'Nhakiwa Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (259, N'Nyakasoro Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (260, N'Nyanzou Clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (261, N'Sowa Rural Health Centre', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (262, N'Tsokodeka clinic', N'clinic', 65, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (263, N'Battlefieds Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (264, N'Bumbe - 100101 - Rural Health Centre', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (265, N'Bururu - 100105 - Council Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (266, N'Chingondo - 100229 - Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (267, N'Cuba RDC Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (268, N'Donain - 100405 - Rural Health Centre', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (269, N'Dondoshava - 100406 - Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (270, N'Gavhunga - 100496 - Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (271, N'Mafindifindi - 100818 - Council Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (272, N'Manyewe - 100878 - Council Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (273, N'Manyoni - 100881 - Council Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (274, N'Mukarati - 101092 - Council Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (275, N'Murambwa - 101125 - Council clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (276, N'Muzvezve - 101191 - Gvt Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (277, N'Ngezi - 101251 - Rural Hosp', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (278, N'Ngezi -101858 -Trauma Centre', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (279, N'St. Michaels - 101646 - Mission Hospital', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (280, N'Turf - 101719 - Council Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (281, N'Twin Tops - 101722 - Clinic', N'clinic', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (282, N'Chalala RDC Clinic', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (283, N'Gache-Gache Rural Health Centre', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (284, N'Kanyati Rural Health Centre', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (285, N'Kariba District Hospital', N'hub', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (286, N'Kasvisva RDC Clinic', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (287, N'Mahombekombe Clinic', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (288, N'Mayovhe RDC clinic', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (289, N'Mola Clinic', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (290, N'Msampakaruma RDC Clinic', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (291, N'Negande Rural Health Centre', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (292, N'Nyamhunga (kab) Clinic', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (293, N'Siyakobvu rural hospital', N'clinic', 32, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (294, N'Bikita Minerals Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (295, N'Bikita Rural Hospital', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (296, N'Chikuku Rural Hospital', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (297, N'Chirorwe Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (298, N'Chitasa Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (299, N'Dewure I Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (300, N'Dewure II Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (301, N'Gangare Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (302, N'Gava Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (303, N'Hozvi Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (304, N'Mandara Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (305, N'Marozva Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (306, N'Mashoko Mission Hospital', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (307, N'Mukanga Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (308, N'Mukore Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (309, N'Mungezi Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (310, N'Murwira Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (311, N'Mutikizizi Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (312, N'Muvava Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (313, N'Negovani Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (314, N'Ngorima Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (315, N'Nyika Rural Health Centre', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (316, N'Odzi Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (317, N'Ruponeso Clinic', N'clinic', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (318, N'Silveira Mission Hospital', N'hub', 41, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (319, N'Binga District Hospital', N'hub', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (320, N'Chinego Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (321, N'Chipale Clinic', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (322, N'Chunga Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (323, N'Kariyangwe Mission Hospital', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (324, N'Lubimbi Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (325, N'Lusulu Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (326, N'Muchesu Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (327, N'Pashu Clinic', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (328, N'Siabuwa Rural Hospital', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (329, N'Siadindi Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (330, N'Siansundu Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (331, N'Simatelele Rural Health Centre', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (332, N'Sinakoma Clinic', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (333, N'Sinansengwe Clinic', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (334, N'Tinde Clinic', N'clinic', 44, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (335, N'Chinotimba Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (336, N'Chisuma RHC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (337, N'Dete RHC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (338, N'Dinde RHC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (339, N'Empumalanga Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (340, N'Hwange Colliery Hospital', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (341, N'Jambezi RHC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (342, N'Kamativi RHC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (343, N'Kanywambizi RHC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (344, N'Lukosi Rural Hospital', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (345, N'Lukunguni Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (346, N'Lupote Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (347, N'Mabale Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (348, N'Main Camp Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (349, N'Milonga Rural Health Center', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (350, N'Mwakandara Rural Health Centre', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (351, N'Mwemba Rural Health Centre', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (352, N'Ndlovu Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (353, N'No 1 Clinic', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (354, N'NO 2 CLINIC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (355, N'NO 3 CLINIC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (356, N'NO 5 CLINIC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (357, N'Sidinda Rural Health Center', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (358, N'Simangane Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (359, N'Songwa RHC', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (360, N'St Patricks Mission Hospital', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (361, N'Victoria Falls District Hospital', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (362, N'Zesa Chibondo Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (363, N'ZESA Ingagula Clinic', N'clinic', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (364, N'Bango - 100042 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (365, N'Dingumuzi - 100394 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (366, N'Embakwe - 100444 - Mission Hospital', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (367, N'Empandeni - 100445 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (368, N'Ingwizi - 100639 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (369, N'Macingwana RHC', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (370, N'Madabe - 100800 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (371, N'Mambale - 100864 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (372, N'Maninji - 101914 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (373, N'Marula - 100910 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (374, N'Matshinge - 100961 - Rural Health Centre', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (375, N'Mayobodo - 100972 - Rural Health Centre', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (376, N'Ndolwane - 101213 - Rural Health Centre', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (377, N'Ntoli - 101303 - Rural Health Centre', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (378, N'Plumtree - 101417 - District Hospital', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (379, N'SANZUKWI - 101529 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (380, N'St. Annes Brunapeg - 101642 - Mission Hospital', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (381, N'Tshitshi - 101712 - Clinic', N'clinic', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (382, N'Chengwena Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (383, N'Chilimanzi Rural Hospital', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (384, N'Chizhou Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (385, N'Denhere Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (386, N'Doroguru Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (387, N'Guramatunhu Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (388, N'Hama Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (389, N'Holy Cross Mission Hospital', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (390, N'Lalapanzi Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (391, N'Lynwood Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (392, N'Mapiravana Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (393, N'Musena Rural Health Centre', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (394, N'Muvonde Mission Hospital', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (395, N'Mvuma District Hospital', N'hub', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (396, N'Nyautonge Rural Health Centre', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (397, N'Nyikavanhu Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (398, N'Siyahokwe Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (399, N'St Theresa Mission Hospital', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (400, N'Tokwe 4 Clinic', N'clinic', 61, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (401, N'Burure Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (402, N'Chireya Mission Hospital', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (403, N'Denda Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (404, N'Gandavaroyi Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (405, N'Gokwe North District Hospital', N'hub', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (406, N'Goredema Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (407, N'Gumunyu Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (408, N'Kadzidirire Rural Health Centre', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (409, N'Kahobo Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (410, N'Kuwirirana Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (411, N'Madzivazvido Rural Health Centre', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (412, N'Mashame Rural Health Centre', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (413, N'Musadzi Rural Health Centre', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (414, N'Mutora Mission Hospital', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (415, N'Nenyunga Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (416, N'Norah Rural Health Centre', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (417, N'Rubatsiro Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (418, N'Simchembu Rural Health Centre', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (419, N'Tsungai Rural Health Centre', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (420, N'Vumba Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (421, N'Zhomba Clinic', N'clinic', 64, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (422, N'Zumba Clinic', N'clinic', 64, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (423, N'Banga Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (424, N'Chikato Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (425, N'Chironde Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (426, N'Chitora Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (427, N'Chrome Mine Hospital', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (428, N'Dorset Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (429, N'Golden Quarry Mine Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (430, N'Gundura Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (431, N'Gwanza Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (432, N'Hanke Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (433, N'Jobolinko Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (434, N'Makusha Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (435, N'Marishongwe Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (436, N'Mazibisa Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (437, N'Nhema Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (438, N'Pakame Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (439, N'Rockford Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (440, N'Ruchanyu Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (441, N'Rusike Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (442, N'Shurugwi District Hospital', N'hub', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (443, N'Svika Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (444, N'Tana Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (445, N'Tokwe Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (446, N'Tongogara Clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (447, N'Zhaugwe Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (448, N'Zvamabande Rural Hospital', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (449, N'Zvarota Rural Health Centre', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (450, N'Zviumwa RDC clinic', N'clinic', 63, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (451, N'Dambudzo Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (452, N'Dayataya RHC Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (453, N'Gudo Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (454, N'Lundi Rural Hospital', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (455, N'Mabasa Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (456, N'Maketo Rural Health Centre', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (457, N'Mandava Health Centre', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (458, N'Mapanzure Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (459, N'Matenda Rural Health Centre', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (460, N'Mhondongori Rural Health Centre', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (461, N'Mimosa Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (462, N'Mrowa Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (463, N'Mtambi Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (464, N'Sabi Mine Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (465, N'Shabani Mine Hospital', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (466, N'Vugwi Rural Health Centre', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (467, N'Vukuzenzele Rural Health Centre', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (468, N'Welezi Clinic', N'clinic', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (469, N'Zvishavane District Hospital', N'hub', 62, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (470, N'Bambanani  New Start Centre', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (471, N'Cowdray Park Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (472, N'Dr. Shennan Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (473, N'E.F. Watson Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (474, N'Emakhandeni Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (475, N'Entumbane Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (476, N'Ingutsheni Central Hospital', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (477, N'Khami Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (478, N'Luveve Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (479, N'Magwegwe Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (480, N'Maqhawe Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (481, N'Mpilo Central Hospital', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (482, N'Mzilikazi Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (483, N'Njube Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (484, N'Nketa Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (485, N'Nkulumane Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (486, N'Northern Suburbs Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (487, N'Pelandaba Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (488, N'Princess Margaret Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (489, N'Pumula Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (490, N'Pumula South Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (491, N'Tshabalala Clinic', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (492, N'United Bulawayo Hospital Central Hospital', N'clinic', 1, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (493, N'Arcadia Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (494, N'Avondale Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (495, N'Beatrice Infectious Hospital', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (496, N'Belvedere Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (497, N'Borrowdale Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (498, N'Braeside Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (499, N'Budiriro Poly Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (500, N'Budiriro Satelite Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (501, N'Caledonia Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (502, N'Chitungwiza General Hospital', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (503, N'Eastly Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (504, N'Epworth Mission Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (505, N'Epworth Poly Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (506, N'Glen Norah Satellite clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (507, N'Glen View  Satellite clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (508, N'Glen View Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (509, N'Greendale Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (510, N'Harare Hospital', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (511, N'Hatcliffe Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (512, N'Hatfield Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (513, N'Highfield Poly Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (514, N'Highlands Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (515, N'Highlands Private Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (516, N'Hopley Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (517, N'Kambuzuma Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (518, N'Kuwadzana Phase 4 Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (519, N'Kuwadzana Poly Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (520, N'Mabelreign satellite clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (521, N'Mabvuku Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (522, N'Mabvuku Poly Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (523, N'Malborough Council Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (524, N'Matapi Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (525, N'Mbare Hostels Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (526, N'Mbare Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (527, N'Mt. Pleasant Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (528, N'Mufakose Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (529, N'New Africa House New Start Centre', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (530, N'Overspill Satellite Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (531, N'Parirenyatwa Central Hospital', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (532, N'Parirenyatwa Primary Care Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (533, N'Rujeko  Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (534, N'Rutsanana Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (535, N'Seke North Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (536, N'Seke South Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (537, N'Southerton Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (538, N'St. Mary''s Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (539, N'Sunningdale Satellite Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (540, N'Tafara Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (541, N'Warren Park Poly clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (542, N'Waterfalls Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (543, N'Western Triangle Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (544, N'Wilkins Infectious Disease Hospital Infectious Disease Hospital', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (545, N'Zengeza Clinic Council Clinic', N'clinic', 3, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (546, N'Bangure Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (547, N'Berenyazvidzi Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (548, N'Betera Rural Health Centre', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (549, N'Birchenough Rural Hospital', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (550, N'Buhera Rural Hospital', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (551, N'Chabata Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (552, N'Chapanduka Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (553, N'Chapwanya Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (554, N'Chawatama Rural Health Centre', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (555, N'Chimbudzi Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (556, N'Chirozva Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (557, N'Chiwenga Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (558, N'Chiweshe Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (559, N'Garamwera Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (560, N'Gombe Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (561, N'Gunura Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (562, N'Madzimbashuro Rural Health Centre', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (563, N'Mombeyarara Rural Health Centre', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (564, N'Mudanda Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (565, N'Mudawose Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (566, N'Munyanyi Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (567, N'Murambinda District Hospital', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (568, N'Murwira Rural Health Centre', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (569, N'Mutepfe Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (570, N'Mutiusinazita Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (571, N'Muzokomba Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (572, N'Nerutanga Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (573, N'Nyashanu Rural Hospital', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (574, N'Rambanapasi Clinic', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (575, N'Zangama Rural Health Centre', N'clinic', 5, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (576, N'ARDA Estates Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (577, N'ARDA Mid-Save Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (578, N'Avontour Tingamire Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (579, N'Chibuwe Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (580, N'Chichichi Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (581, N'Chikore Mission Hospital', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (582, N'Chinyamukwaka Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (583, N'Chipangayi Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (584, N'Chipinge District Hospital', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (585, N'Chipinge Town Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (586, N'Chiriga Rural Health Centre', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (587, N'Chisuma Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (588, N'Clear Water Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (589, N'Gaza Council Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (590, N'Gumira  Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (591, N'Gwenzi Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (592, N'Hwakata Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (593, N'Jersey Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (594, N'Junction Gate Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (595, N'Kondo Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (596, N'Kopera Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (597, N'Mabeye Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (598, N'Madhuka Rural Health Centre', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (599, N'Mahenye Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (600, N'Manzvire Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (601, N'Mt. Selinda Mission Hospital', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (602, N'Muparadze Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (603, N'Musani Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (604, N'Musirwizi Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (605, N'Muswera Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (606, N'Mutandahwe Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (607, N'Mutema Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (608, N'New Year Gift Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (609, N'Ngaome Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (610, N'Nyunga Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (611, N'Paidamoyo Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (612, N'Ratelshoek Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (613, N'Rimbi Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (614, N'Silverstream Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (615, N'Southdowns Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (616, N'St. Peters Mission Hospital', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (617, N'Tamandai Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (618, N'Tanganda Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (619, N'Tongogara Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (620, N'Tuzuka Rural Health Centre', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (621, N'Vheneka Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (622, N'Zamchiya Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (623, N'Zona Clinic', N'clinic', 7, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (624, N'Anorldine Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (625, N'Bamba Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (626, N'Chiduku Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (627, N'Chikobvore Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (628, N'Chikore Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (629, N'Chinhenga Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (630, N'Chinyadza Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (631, N'Chinyika 1 Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (632, N'Chinyika 2 Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (633, N'Chinyudze Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (634, N'Chitungwiza Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (635, N'Dowa Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (636, N'Dumbamwe Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (637, N'Era Mine Mine Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (638, N'Gorubi Springs Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (639, N'Gowakowa Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (640, N'Headlands Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (641, N'Katsenga Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (642, N'Makoni Rural Hospital', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (643, N'Maparura Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (644, N'Masvosva Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (645, N'Matotwe Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (646, N'Matsika Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (647, N'Maurice Nyagumbo Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (648, N'Mayo 1 Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (649, N'Mayo 2 Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (650, N'Mubvurungwa Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (651, N'Mufusire Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (652, N'Mukamba Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (653, N'Mukuwapasi Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (654, N'Nasmie Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (655, N'Nedevedzo Rural Hospital', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (656, N'Nedziwa Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (657, N'Nyahowe Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (658, N'Nyahukwe Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (659, N'Nyamidzi Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (660, N'Nyamukamani Rural Health Centre', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (661, N'Nyamusosa Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (662, N'Nyazura Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (663, N'Nyazura Mission Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (664, N'Ringanayi Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (665, N'Rukweza Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (666, N'Rusape District Hospital', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (667, N'Sangano Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (668, N'St. Michael''s Mission Hospital', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (669, N'St. Theresa Mission Hospital', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (670, N'Tandi Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (671, N'Tariro Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (672, N'Tsanzaguru Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (673, N'Vengere Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (674, N'Weya Rural Hospital', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (675, N'Zunidza Clinic', N'clinic', 8, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (676, N'ARDA Odzi Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (677, N'ARDA Transau  Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (678, N'Bakorenhema Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (679, N'Berzerly Bridge Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (680, N'Burma Valley Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (681, N'Bwizi Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (682, N'Chiadzwa Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (683, N'Chikanga Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (684, N'Chikwariro Mission Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (685, N'Chipendeke Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (686, N'Chipfatsura Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (687, N'Chishingwi Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (688, N'Chitaka Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (689, N'Chitakatira Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (690, N'Chitora Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (691, N'Chiwere Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (692, N'Dangamvura Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (693, N'Dora Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (694, N'Fernvalley Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (695, N'Florida Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (696, N'Gutaurare Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (697, N'Gwindingwi Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (698, N'Hob House  Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (699, N'Lee Kul Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (700, N'Mambwere Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (701, N'Marange Rural Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (702, N'Masasi Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (703, N'Matanda Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (704, N'Mavhiza Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (705, N'Mt. Zuma Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (706, N'Mukwada Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (707, N'Munyarari Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (708, N'Muromo Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (709, N'Mushunje Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (710, N'Mutare Council Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (711, N'Mutare New Start Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (712, N'Mutare Provincial Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (713, N'Nyagundi Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (714, N'Nyamazura Rural Health Centre', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (715, N'Nzvenga Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (716, N'Odzi Rural Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (717, N'Rowa Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (718, N'Sakubva District Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (719, N'Sakubva Health Centre Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (720, N'St. Andrew''s Mission Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (721, N'St. Joseph''s T.B Hospital', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (722, N'St. Welburgh Mission Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (723, N'Vumba Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (724, N'Zimunya Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (725, N'Zumbare Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (726, N'Zvipiripiri Clinic', N'clinic', 9, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (727, N'Bonda Mission Hospital', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (728, N'Chavhanga Rural Health Centre', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (729, N'Chinamasa Rural Health Centre', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (730, N'Chisuko Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (731, N'Chitombo Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (732, N'Drenane Timbers Private Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (733, N'Eastern Highlands 1 Private Tanganda', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (734, N'Gatsi Mission Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (735, N'Guta Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (736, N'Haparare Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (737, N'Hauna Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (738, N'Hauna District Hospital', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (739, N'Honde Mission Hospital', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (740, N'Jombe Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (741, N'Katiyo Private-Tanganda', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (742, N'Mandeya 11 Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (743, N'Mapara Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (744, N'Moyoweshumba Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (745, N'Mt. Jenya Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (746, N'Mupotedzi Gvt Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (747, N'Mutasa Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (748, N'Ngarura Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (749, N'Nyanga Pines Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (750, N'Old Mutare Mission Hospital', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (751, N'Premier Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (752, N'Red Wing Private-Mine', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (753, N'Rupinda Rural Health Centre', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (754, N'Sachisuko Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (755, N'Sadziwa Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (756, N'Sagambe Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (757, N'Sahumani Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (758, N'Sakupwanya Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (759, N'Samanga Council clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (760, N'Samaringa Council clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (761, N'Selbourne Wattle Company Private Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (762, N'Sheba Border Timbers Private Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (763, N'Sherukuru Rural Health Centre', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (764, N'St. Augustine''s Mission Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (765, N'St. Barbara''s Mission Hospitals', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (766, N'St. Peter''s Mandeya Mission Hospital', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (767, N'Triashill Mission Hospitals', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (768, N'Tsonzo Rural Hospital', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (769, N'Zindi Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (770, N'Zongoro Council Clinic', N'clinic', 10, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (771, N'Angwa Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (772, N'Bakasa Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (773, N'Bepura Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (774, N'Birkdale Rural Health Centre', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (775, N'Brandon Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (776, N'Bvochora Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (777, N'Chapoto Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (778, N'Chidodo Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (779, N'Chikafa Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (780, N'Chipuriro Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (781, N'Chirunya Rural Health Centre', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (782, N'Chitsungo District Hospital', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (783, N'Gonono Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (784, N'Gota Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (785, N'Guruve Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (786, N'Guruve District Hospital', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (787, N'Kachuta Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (788, N'Kamusasa Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (789, N'Kemutamba Rural Health Centre', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (790, N'Mahuwe Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (791, N'Masoka Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (792, N'Masomo Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (793, N'Matsvitsi Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (794, N'Msengezi Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (795, N'Mugarakamwe Rural Health Centre', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (796, N'Mushumbi Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (797, N'Negomo Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (798, N'Nyakapupu Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (799, N'Nyambudzi Rural Health Centre', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (800, N'Nyamhondoro Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (801, N'Ruyamuro Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (802, N'Shinje Clinic', N'clinic', 13, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (803, N'Ardura Rural Health Centre', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (804, N'Bare Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (805, N'Belgone Clinic Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (806, N'Chinehasha Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (807, N'Christon Bank Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (808, N'Concession  District Hospital', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (809, N'Dambo Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (810, N'Davaar Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (811, N'Donje Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (812, N'Forrester Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (813, N'Henderson Research Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (814, N'Holmeden Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (815, N'Howard Mission Hospital', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (816, N'Iron Duke Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (817, N'Jingamvura Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (818, N'Makope Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (819, N'Mazowe Citrus Hosp. Rural Hospital', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (820, N'Mazowe Mine Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (821, N'Mvurwi Hospital', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (822, N'Nyakudya Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (823, N'Nzvimbo Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (824, N'Rosa Rural Hospital', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (825, N'Shopo Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (826, N'Shutu Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (827, N'Tsungubvi Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (828, N'Vonabor Clinic', N'clinic', 14, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (829, N'Bandimba Rural Health Centre', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (830, N'Bveke Clinic (New', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (831, N'Chawanda Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (832, N'Chitepo Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (833, N'Chitse Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (834, N'Dotito Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (835, N'Kaitano Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (836, N'Kamutsenzere Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (837, N'Karanda Mission Hospital', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (838, N'Matope Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (839, N'Mt. Darwin District Hospital', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (840, N'Mukumbura Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (841, N'Mutasa Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (842, N'Mutungagore Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (843, N'Nembire Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (844, N'Nyamahobobo Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (845, N'Pachanza Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (846, N'Pfunyanguwo Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (847, N'Tsakare Clinic', N'clinic', 66, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (848, N'Arcturus Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (849, N'Bosha Rural Health Centre', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (850, N'Bromley Rural Health Centre', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (851, N'Chikwaka Rural Hospital', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (852, N'Chinamhora Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (853, N'Chinyika Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (854, N'Cranborne Clinic Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (855, N'Domboshava Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (856, N'Gejo raRuby Rural Health Centre', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (857, N'Joan Rankini Rural Health Centre', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (858, N'John Reimer Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (859, N'Kowoyo Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (860, N'Kubatsirana Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (861, N'Makumbe District Hospital', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (862, N'Masukandoro Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (863, N'Melfort Rural Health Centre', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (864, N'Mwanza Rural Health Centre', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (865, N'Nyaure Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (866, N'Pote Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (867, N'Rusike Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (868, N'Ruwa Poly Clinic', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (869, N'Ruwa Rehabilitation  Hospital', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (870, N'St. Joseph''s Rural Health centre', N'clinic', 28, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (871, N'Border Church Rural Health Centre', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (872, N'Chimbwanda Rural Health Centre', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (873, N'Chiota Rural Hospital', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (874, N'Chiparawe Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (875, N'Dimbiti Rural Health Centre', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (876, N'Dombotombo Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (877, N'Igava Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (878, N'Kushinga Phikelela Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (879, N'Lustliegh Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (880, N'Mahusekwa Hospital', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (881, N'Marondera  Provincial Hospital', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (882, N'Marondera Rural Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (883, N'Masikana Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (884, N'Mudzimuirema Rural Health Centre', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (885, N'Nyameni Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (886, N'Nyembanzvere Clinic', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (887, N'Wenimbe Rural Health Centre', N'clinic', 27, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (888, N'Chitate Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (889, N'Chitowa 1 Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (890, N'Chitowa 2 Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (891, N'Craiglea Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (892, N'Dandara Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (893, N'Dombwe Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (894, N'Goso Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (895, N'Jekwa Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (896, N'Kadenge Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (897, N'Kadzere Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (898, N'Kambarami Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (899, N'Macheke Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (900, N'Madamombe Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (901, N'Matututu Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (902, N'Muchinjike Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (903, N'Munamba Rural Health Centre', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (904, N'Murewa District Hospital', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (905, N'Murewa Poly Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (906, N'Ngwerume Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (907, N'Nhowe Mission Hospital', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (908, N'Nyamutumbu Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (909, N'Shambamuto Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (910, N'St. Paul''s Musami Mission Hospital', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (911, N'Virginia Clinic Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (912, N'Waterloo Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (913, N'Welcome Home Liden Clinic', N'clinic', 67, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (914, N'Beersheba Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (915, N'Brunswick Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (916, N'Chegutu District Hospital', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (917, N'Chegutu Urban Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (918, N'Chikara Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (919, N'Chinengundu Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (920, N'Chivero Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (921, N'Dombwe  Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (922, N'Gora Rural Health Centre', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (923, N'Homedale Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (924, N'Katanga utano Municipality', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (925, N'Lizmore Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (926, N'Mafuti Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (927, N'Mbuyanehanda Rural Health Centre', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (928, N'Mhondoro North Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (929, N'Mhondoro Rural Hospital', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (930, N'Monera Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (931, N'Mupawose Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (932, N'Musinami Rural Health Centre', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (933, N'Norton Hospital', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (934, N'Pfupajena Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (935, N'Presbyterian  Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (936, N'Rwizi Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (937, N'Sandringham Mission Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (938, N'Santa Barbra Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (939, N'Selous Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (940, N'Shamrock Clinic (Not Yet Open)', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (941, N'Watyoka Council Clinic', N'clinic', 35, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (942, N'Chibara Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (943, N'Chidamoyo Mission Hospital', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (944, N'Chinhere Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (945, N'Chirundu Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (946, N'Chivende Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (947, N'Chundu Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (948, N'Dete Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (949, N'Deve Clinic (New', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (950, N'Doro Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (951, N'Hesketh Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (952, N'Hewiyai Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (953, N'Hurungwe Rural Hospital', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (954, N'Kapfunde Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (955, N'Karoi District Hospital', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (956, N'Karoi Static Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (957, N'Karuru Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (958, N'Kasimube Rural Health Centre', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (959, N'Kazangarare Gvt Council', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (960, N'Lan Lorry Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (961, N'Lynx Clinic Private Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (962, N'Makuti Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (963, N'Masanga Gvt Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (964, N'Mashongwe Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (965, N'Murambi Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (966, N'Mwami Hospital', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (967, N'Nyama Council', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (968, N'Nyamakaze Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (969, N'Nyamhunga Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (970, N'Nyangoma Council Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (971, N'Tengwe Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (972, N'Zebra Downs Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (973, N'Zvipani Clinic', N'clinic', 34, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (974, N'Black Movale Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (975, N'Bumbe Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (976, N'Bururu Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (977, N'Chakari Mine Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (978, N'Chegutu 6 Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (979, N'Chemukute Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (980, N'Chingondo Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (981, N'Chirikiti Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (982, N'Donain Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (983, N'Dondoshava Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (984, N'Gavhunga Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (985, N'Golden Valley Private Mine Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (986, N'Jompani Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (987, N'Kadoma District Hosp', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (988, N'Mafindifindi Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (989, N'Manyewe Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (990, N'Manyoni Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (991, N'Mukarati Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (992, N'Murambwa Council clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (993, N'Muuyu Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (994, N'Muzvezve Gvt Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (995, N'New Geja Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (996, N'Ngezi Rural Hosp', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (997, N'Ngezi Trauma Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (998, N'Nyabango Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (999, N'Nyamatani Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1000, N'Nyaonde Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1001, N'Ordoff Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1002, N'Patchway Mine Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1003, N'Rimuka Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1004, N'Sanyati Area Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1005, N'Sanyati Mission Hospital', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1006, N'St. Michaels Mission Hospital', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1007, N'Turf Council Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1008, N'Twin Tops Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1009, N'Vere Rural Health Centre', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1010, N'Waverly Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1011, N'Zimplats Ngezi Private Clinic', N'clinic', 68, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1012, N'Alaska Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1013, N'Chikonohono Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1014, N'Chinhoyi  Provincial Hospital', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1015, N'Chinhoyi Clinic Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1016, N'Doma Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1017, N'Gamanya Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1018, N'Godzi Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1019, N'Green Valley Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1020, N'Gudubu Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1021, N'Hombwe Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1022, N'Kamonde Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1023, N'Kanyanga Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1024, N'Kenzamba Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1025, N'Kosana Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1026, N'Long Valley Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1027, N'Makonde Christian Mission Hospital', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1028, N'Manyamba Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1029, N'Matorangera Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1030, N'Mukohwe Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1031, N'Murereka Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1032, N'Nyamugomba Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1033, N'Obva Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1034, N'Portlet Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1035, N'River Ranch Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1036, N'Runene  Council Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1037, N'Sadoma Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1038, N'Shackleton Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1039, N'St. Rupert''s Mission Hospital', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1040, N'Umboe Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1041, N'Zumbara Clinic', N'clinic', 30, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1042, N'ARDA Sisi Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1043, N'Ayrshire Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1044, N'Banket District Hospital', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1045, N'Bevking  Private Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1046, N'Chirau Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1047, N'Chivhere Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1048, N'Darwendale Rural Hospital', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1049, N'Dzivarasekwa Extension Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1050, N'Father O''Hea Mission Hospital', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1051, N'Gwebi Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1052, N'Jari Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1053, N'Kemurara Rural Health Centre', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1054, N'Kutama Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1055, N'Kuwadzana Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1056, N'Lospen Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1057, N'Madzorera Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1058, N'Mapinga  Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1059, N'Masiyarwa Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1060, N'Mpumbu  Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1061, N'Mt. Hampden Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1062, N'Muriel Mine Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1063, N'Mutorashanga Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1064, N'Nyabika Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1065, N'Raffingora Rural Hospital', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1066, N'Sutton Mine Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1067, N'TRBC Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1068, N'Trelawney Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1069, N'Vanad Mine Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1070, N'Zowa Council Clinic', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1071, N'Zvimba Rural Hospital', N'clinic', 29, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1072, N'Chambuta Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1073, N'Chikombedzi Hospital', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1074, N'Chilonga Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1075, N'Chimbwedziva Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1076, N'Chingele Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1077, N'Chipiwa Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1078, N'Chiredzi Hospital', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1079, N'Chitsa Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1080, N'Chizvirizvi Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1081, N'Chomopani Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1082, N'Damarakanaka Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1083, N'Davata Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1084, N'Dumisa Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1085, N'Faversham Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1086, N'Gezani Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1087, N'Hippo Valley Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1088, N'Makambe Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1089, N'Malipati Rural Health Centre', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1090, N'Mkwasine Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1091, N'Muteyo Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1092, N'Nyangambe Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1093, N'Old Boli Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1094, N'Pahlela Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1095, N'Porepore Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1096, N'Rapanguwana Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1097, N'Rutandare Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1098, N'Samu Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1099, N'St. Joseph Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1100, N'Triangle Hospital', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1101, N'Tsovani Clinic', N'clinic', 42, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1102, N'Berejena Mission Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1103, N'Chidyamakono Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1104, N'Chifedza Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1105, N'Chigwikwi Rural Health Centre', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1106, N'Chirongwe Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1107, N'Chivi District Hospital', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1108, N'Chivi Mission Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1109, N'Chivi Rural Hospital', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1110, N'Davira Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1111, N'Gororo Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1112, N'Madamombe Rural Health Centre', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1113, N'Madzivadondo Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1114, N'Masinire Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1115, N'Mhandamabwe Rural Health Centre', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1116, N'Ngundu Rural Health Centre', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1117, N'Nyahombe Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1118, N'Razi Rural Health Centre', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1119, N'Shindi Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1120, N'Takavarasha Rural Health Centre', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1121, N'Utete Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1122, N'Varanda Rural Health Centre', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1123, N'Ziviku Clinic', N'clinic', 36, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1124, N'Chepiri Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1125, N'Cheshuro Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1126, N'Chimombe Rural Hospital', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1127, N'Chinyika Rural Health Centre', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1128, N'Chitando Rural Health Centre', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1129, N'Chiwore Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1130, N'Dambara Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1131, N'Denhere Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1132, N'Devure Mission Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1133, N'Gutu Mission Hospital', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1134, N'Gutu Rural  Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1135, N'Magombedze Chitsa Rural Health Centre', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1136, N'Magombedze Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1137, N'Majarada Rural Health Centre', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1138, N'Mataruse Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1139, N'Matizha Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1140, N'Mazura Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1141, N'Mukaro Mission Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1142, N'Munyikwa Rural Health Centre', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1143, N'Mushaviri Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1144, N'Mutema Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1145, N'Mutero Mission Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1146, N'Nemashakwe Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1147, N'Nyazvidzi Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1148, N'Serima Mission Hospital', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1149, N'Soti Source Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1150, N'Tirizi Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1151, N'Zinhata Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1152, N'Zvavahera Clinic', N'clinic', 37, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1153, N'Alvod Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1154, N'Bere Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1155, N'Bondolfi Rural Hospital', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1156, N'Charumbira Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1157, N'Chatikobo Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1158, N'Gaths Mine Hospital', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1159, N'Gokomere Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1160, N'Gundura Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1161, N'Gurajena Hospital', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1162, N'Guwa Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1163, N'Hwendedzo Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1164, N'Mapanzure Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1165, N'Masvingo General Hospital', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1166, N'Masvingo New Start Centre', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1167, N'Mogenester Mission Hospital', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1168, N'Mucheke Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1169, N'Mukosi Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1170, N'Murinye Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1171, N'Mushandike Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1172, N'Musvovi Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1173, N'Nemwanwa Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1174, N'Ngomahuru Rural Health Centre', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1175, N'Nyajena Rural Hospital', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1176, N'Nyamande Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1177, N'Nyikavanhu Rural Health Centre', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1178, N'Renco Mine Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1179, N'Rujeko Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1180, N'Rukovo Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1181, N'Runyararo Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1182, N'Shonganiso Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1183, N'Shumba Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1184, N'Summerton Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1185, N'Zano Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1186, N'Zimuto BC Clinic', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1187, N'Zimuto Mission Hospital', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1188, N'Zvamahande Rural Health Centre', N'clinic', 38, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1189, N'Boterere Rural Health Centre', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1190, N'Chimbudzi Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1191, N'Chingwizi Satelite Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1192, N'Chirindi Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1193, N'Chizumba Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1194, N'G&N Clinic Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1195, N'Lundi Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1196, N'Maranda Mission Hospital', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1197, N'Maranda Sub-Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1198, N'Marinda Rural Health Centre', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1199, N'Matibi Mission Hospital', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1200, N'Mazetese Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1201, N'Mulelesi Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1202, N'Munyanyi Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1203, N'Murove Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1204, N'Mushava Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1205, N'Mwenezana Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1206, N'Mwenezi Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1207, N'Nehanda Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1208, N'Neshuro District Hospital', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1209, N'Rutenga Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1210, N'Rutenga Railways Clinic', N'clinic', 39, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1211, N'Bota Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1212, N'Bvukururu Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1213, N'Chinyabako Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1214, N'Chipinda Rural Health Centre', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1215, N'Chiredzana Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1216, N'Fuve Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1217, N'Harava Rural Health Centre', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1218, N'Jerera Satelite Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1219, N'Jichidza Council Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1220, N'Jichidza Mission Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1221, N'Mageza Rural Health Centre', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1222, N'Mandhloro Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1223, N'Mushaya Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1224, N'Musiso Mission Hospital', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1225, N'Ndanga Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1226, N'Ndanga Hospital', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1227, N'Nemauku Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1228, N'Nhema Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1229, N'Nyakunhuwa Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1230, N'Siyawareva Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1231, N'Svuvure Rural Health Hospital', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1232, N'Veza Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1233, N'Zibwowa Private Clinic', N'clinic', 40, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1234, N'Chinego RHC', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1235, N'Chunga', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1236, N'Kariyangwe', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1237, N'Lubimbi', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1238, N'Lusulu', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1239, N'Mucheso', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1240, N'Ngumija', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1241, N'Pashu', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1242, N'Siabuwa', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1243, N'Siadindi', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1244, N'Siansundu', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1245, N'Simatelele', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1246, N'Sinakoma', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1247, N'Sinansengwe', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1248, N'Tinde', N'clinic', 44, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1249, N'Balanda Rural Health Centre', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1250, N'Inyathi District Hospital', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1251, N'Kenilworth Rural Health Centre', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1252, N'Lukala Rural Health Centre', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1253, N'Madambe Clinic', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1254, N'Majiji Clinic', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1255, N'Mbembeswane', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1256, N'Mdutshane Clinic', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1257, N'Raafs Rural Health Centre', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1258, N'Sicanda Rural Health Centre', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1259, N'Turk Mine Clinic', N'clinic', 45, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1260, N'5 Miles', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1261, N'BAPZ', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1262, N'Breakfast', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1263, N'Chibondo', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1264, N'Chikandakubi', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1265, N'Chinotimba', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1266, N'Chisuma', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1267, N'Colliery', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1268, N'Dete', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1269, N'Dinde', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1270, N'Elephant Hills', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1271, N'Empumalanga', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1272, N'Ingagula', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1273, N'Jabula', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1274, N'Jambezi', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1275, N'Kamativi', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1276, N'Kanywambizi', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1277, N'Lubangwe', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1278, N'Lukosi', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1279, N'Lukunguni', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1280, N'Lupote', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1281, N'Mabale', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1282, N'Makwandara', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1283, N'Matetsi', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1284, N'Milonga', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1285, N'Mwemba', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1286, N'Ndimakule', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1287, N'Ndlovu', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1288, N'No 2 Clinic', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1289, N'No. 5 Clinic', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1290, N'NRZ Clinic', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1291, N'Premier clinic', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1292, N'PSMI Hwange', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1293, N'Sidinda', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1294, N'Simangani', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1295, N'Songwe', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1296, N'St Patricks', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1297, N'THB', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1298, N'V.F Hotel Clinic', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1299, N'V.F Prison clinic', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1300, N'Victoria Falls Hospital', N'hub', 46, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1301, N'Wilderness', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1302, N'Woodlands', N'clinic', 46, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1303, N'Dandanda Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1304, N'Dongamuzi Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1305, N'Fatima Mission Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1306, N'Gomoza Rural Health Centre', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1307, N'Gwaai RHC', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1308, N'Jotsholo Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1309, N'Kanyandavu Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1310, N'Lake Alice Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1311, N'Lupaka Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1312, N'Lupane Rural Health Centre', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1313, N'Mdlankunzi Clinic', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1314, N'St. Lukes Mission Hospital', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1315, N'St. Pauls Mission Hospital', N'clinic', 47, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1316, N'Dakamela Rural Hospital', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1317, N'Fanison Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1318, N'Guwe Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1319, N'Gwelutshena Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1320, N'Lutsha RHC', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1321, N'Mateme Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1322, N'Mbuma Mission Hospital', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1323, N'Nesigwe Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1324, N'Ngwaladi Rural Hospital', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1325, N'Nkayi District Hospital', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1326, N'Satelite clinic', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1327, N'Sebumane Clinic', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1328, N'Sesemba Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1329, N'Sikhobokhobo Clinic', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1330, N'Sivalo Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1331, N'Vova RHC', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1332, N'Zenka Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1333, N'Zinyangeni Rural Health Centre', N'clinic', 48, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1334, N'Bemba Council Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1335, N'Bubude RHC', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1336, N'Dlamini Council Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1337, N'Jimila Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1338, N'Kapane RHC', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1339, N'Madlangombe  Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1340, N'Makaza Rural Health Centre', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1341, N'Mlagisa Rural Health centre', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1342, N'Mpanedziba Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1343, N'Mtshayeli Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1344, N'Nkunzi Rural Health Centre', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1345, N'Pumula Mission Hospital', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1346, N'Samahuru Mission clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1347, N'Shaba Council Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1348, N'Sikente Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1349, N'Sipepa Rural Hospital', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1350, N'Sodaka Rural Health centre', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1351, N'Tshefunye', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1352, N'Tsholotsho District Hospital', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1353, N'Tsholotsho Urban Clinic', N'clinic', 49, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1354, N'Anju', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1355, N'Fairbridge ZRP Camp clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1356, N'Fingo Clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1357, N'Igusi Rural Health Centre', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1358, N'Imbizo Barracks ZNA Hospital', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1359, N'Lozikeyi Clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1360, N'Mbembesi Rural Health Centre', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1361, N'Ntabazinduna Clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1362, N'Nyamandlovu District Hospital', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1363, N'Redwood Clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1364, N'Ross camp', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1365, N'Siganda   Clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1366, N'St. James Mission Clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1367, N'T.G. Silundika Rural Health Centre', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1368, N'Umguza RDC Clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1369, N'Umuntu clinic', N'clinic', 43, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1370, N'Beitbridge District Hospital', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1371, N'Chamunangana Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1372, N'Chasvingo Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1373, N'Chikwarakwara Rural Health Centre', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1374, N'Chituripasi Rural Health Centre', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1375, N'Dite Rural Health Centre', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1376, N'Dulibadzimu Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1377, N'Majini Rural Health Centre', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1378, N'Makakabule Rural Health Centre', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1379, N'Makombe Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1380, N'Masera Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1381, N'Mtetengwe Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1382, N'Nottingham Rural Health Centre', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1383, N'Shabwe Rural Health Centre', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1384, N'Shashe Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1385, N'Swereki Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1386, N'Tongwe Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1387, N'Zezane Clinic', N'clinic', 51, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1388, N'Bezu Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1389, N'Dombodema Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1390, N'Hingwe Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1391, N'Huwana Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1392, N'Lady Barring Mission Hospital', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1393, N'Lady Stanley Mission Hospital', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1394, N'Madlambuzi Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1395, N'Makhuleka Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1396, N'Masendu Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1397, N'Matjinge  Rural Health Centre', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1398, N'Ndiweni Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1399, N'Nswazwi Rural Health Centre', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1400, N'Sikhatini Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1401, N'Solusi Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1402, N'Tokwana Clinic', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1403, N'Village 13 Rural Health Centre', N'clinic', 50, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1404, N'Buvuma Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1405, N'Garanyemba Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1406, N'Gungwe Rural Health Centre', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1407, N'Gwanda  Provincial Hospital', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1408, N'Kafusi Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1409, N'Lushongwe Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1410, N'Makwe Rural Health Centre', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1411, N'Manama Mission Hospital', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1412, N'Mapate Cliniclinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1413, N'Mashaba Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1414, N'Mtshabezi Mission Hospital', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1415, N'Mzimuni Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1416, N'Nhwali Rural Health Centre', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1417, N'Ntalale Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1418, N'Pakama Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1419, N'Selonga Rural Health Centre', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1420, N'Sengwezani Rural Health Centre', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1421, N'Silkwe Rural Health centre', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1422, N'Simbumbumbu Rural Health Centre', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1423, N'Sitezi clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1424, N'Stanmore Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1425, N'West Nicolson Clinic', N'clinic', 52, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1426, N'Avoca Rural Hospital', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1427, N'Filabusi District Hospital', N'lab', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1428, N'Gwatemba Rural Health Centre', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1429, N'Insiza PBS  Clinic', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1430, N'Kombo Clinic', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1431, N'Mabuze Rural Health Centre', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1432, N'Nkankezi Rural Health Centre', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1433, N'Nyamime Rural Health Centre', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1434, N'Sanale Rural Health Centre', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1435, N'Saphila Council Clinic(Construction)', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1436, N'Shangani Mine Clinic', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1437, N'Shangani Rural Hospital', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1438, N'Singwambizi Clinic', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1439, N'Singwango Clinic', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1440, N'Wanezi Rural Hospital', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1441, N'Zhulube Clinic', N'clinic', 53, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1442, N'Bango Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1443, N'Dingumuzi Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1444, N'Embakwe Mission Hospital', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1445, N'Empandeni Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1446, N'Ingwizi Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1447, N'Madabe Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1448, N'Mambale Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1449, N'Maninji Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1450, N'Marula Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1451, N'Mayobodo Rural Health Centre', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1452, N'Plumtree District Hospital', N'hub', 56, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1453, N'SANZUKWI Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1454, N'St. Annes Brunapeg Mission Hospital', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1455, N'Tshitshi Clinic', N'clinic', 56, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1456, N'Bazha Clinic', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1457, N'Beula Rural Health Centre', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1458, N'Cyrene Mission Clinic', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1459, N'Ekukanyeni Clinic', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1460, N'Gulati Rural Health Centre', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1461, N'Homestead Rural Health Centre', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1462, N'Kezi Rural Hospital', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1463, N'Maphisa District Hospital', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1464, N'Masiye Camp Clinic', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1465, N'Matobo Mission Clinic', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1466, N'Matobo Rural Rural Hospital', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1467, N'Mbembeswane Rural Health Centre', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1468, N'Natisa Rural Health Centre', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1469, N'Sankonjana Rural Health Centre', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1470, N'St. Joseph''s Rural Hospital', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1471, N'Tshelanyemba Mission Hospital', N'clinic', 54, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1472, N'Empsini  Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1473, N'Esibobvu Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1474, N'Esigodini District Hospital', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1475, N'Habani Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1476, N'How Mine Mine Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1477, N'Irisvale Rural Health Centre', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1478, N'Kumbuzi Rural Health Centre', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1479, N'Mawabeni Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1480, N'Mbizingwe Rural Health Centre', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1481, N'Mhlahlandlela Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1482, N'Mpisini Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1483, N'Nhlangano Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1484, N'Nswazi Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1485, N'Ntshamathe Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1486, N'Umzingwane Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1487, N'Zimbili Clinic', N'clinic', 55, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1488, N'Chemahororo Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1489, N'Cheziya Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1490, N'Chitave Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1491, N'Gawa Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1492, N'Gokwe District Hospital', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1493, N'Gwanyika Rural Health Centre', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1494, N'Huchu Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1495, N'Jahana Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1496, N'Jiri Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1497, N'Kana Mission Hospitals', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1498, N'Krima Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1499, N'Mangidi Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1500, N'Manoti Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1501, N'Manyoni Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1502, N'Masuka Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1503, N'Mateme Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1504, N'Mateta Rural Health Centre', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1505, N'Mkoka Rural Health Centre', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1506, N'Msala Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1507, N'Musita Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1508, N'Mutange Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1509, N'Ndabambi Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1510, N'Njelele Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1511, N'Nyaje Rural Health Centre', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1512, N'Nyamunga Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1513, N'Sai Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1514, N'Sesame Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1515, N'Svisvi Rural Health Centre', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1516, N'Tongwe Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1517, N'Zhamba Clinic', N'clinic', 57, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1518, N'Chikwingwizha Mission Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1519, N'Child Welfare Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1520, N'Chinamasa Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1521, N'Chiundura Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1522, N'Gunde Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1523, N'Gweru  Provincial Hospital', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1524, N'Gweru District Hospital', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1525, N'Gweru New Start Centre/New Life Centre', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1526, N'Hozheri Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1527, N'Ivene Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1528, N'Kabanga Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1529, N'Lower Gweru Mission Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1530, N'Maboleni Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1531, N'Madhikani Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1532, N'Makepesi Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1533, N'Mangwande Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1534, N'Masvori Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1535, N'Mkoba 1 Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1536, N'Mkoba Poly Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1537, N'Monomutapa Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1538, N'Ntabamhlope Rural Health Centre', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1539, N'Nyama Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1540, N'Ruby Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1541, N'Senga Poly Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1542, N'Somabula Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1543, N'St. Patricks Mission Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1544, N'Totonga Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1545, N'Tumbire Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1546, N'Vungu Clinic', N'clinic', 58, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1547, N'Al Davies Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1548, N'Amaveni Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1549, N'Dambridge Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1550, N'Dendera Rural Hospital', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1551, N'Don Juan Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1552, N'Donsa Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1553, N'Exchange Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1554, N'Gomola Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1555, N'Jena Mine Mine Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1556, N'Kwekwe District Hospital', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1557, N'Malisa  Zhambe   Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1558, N'Malisa Josefa Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1559, N'Mayoka Rural Health Centre', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1560, N'Mazebe Rural Health Centre', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1561, N'Mbizo 1 Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1562, N'Mbizo 2 Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1563, N'Mlezu College Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1564, N'Mpinda Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1565, N'Msilahove Rural Hospital', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1566, N'Munyati Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1567, N'Ntabeni Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1568, N'Nyoni Rural Health Centre', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1569, N'Redcliff Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1570, N'Rio Tinto Mine Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1571, N'Rutendo Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1572, N'Samambwa Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1573, N'Sebakwe Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1574, N'Senkwasi Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1575, N'Sherwood Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1576, N'Sidakeni Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1577, N'Sigezububi Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1578, N'Silobela District Hospital', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1579, N'Silobela Jackson Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1580, N'Simana Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1581, N'Torwood Hospital', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1582, N'Zhombe Mission Clinic', N'clinic', 59, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1583, N'Bonda Mission Hospital', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1584, N'Buchwa Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1585, N'Chabwira Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1586, N'Chaza  Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1587, N'Chedembeko Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1588, N'Chiedza Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1589, N'Chingezi Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1590, N'Gaha Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1591, N'Gwarava Rural Health Centre', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1592, N'Imbahuru Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1593, N'Ingezi Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1594, N'Jeka Rural Hospital', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1595, N'Kotokwe Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1596, N'Makuwerere Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1597, N'Masase Mission Hospital', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1598, N'Mataga Rural Health Centre', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1599, N'Matedzi Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1600, N'Mavorovondo Rural Health Centre', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1601, N'Mazivofa Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1602, N'Mberengwa District Hospital', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1603, N'Mnene Mission Hospital', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1604, N'Mponjani Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1605, N'Mposi Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1606, N'Muketi Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1607, N'Murongwe Rural Health Centre', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1608, N'Musume Mission Hospital', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1609, N'Mwenezi Rural Health Centre', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1610, N'Negobe Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1611, N'Ngungumbane Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1612, N'Sandawana Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1613, N'Svita Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1614, N'Vurasha Rural Health Centre', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1615, N'Vutsanana Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1616, N'Wanezi Clinic', N'clinic', 60, N'DSD', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1617, N'Beatrice Infectious - 100050 - Hospital', N'lab', 3, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1618, N'Bindura - 100070 - Provincial Hospital', N'lab', 15, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1619, N'Chinhoyi  - 100235 - Provincial Hospital', N'lab', 30, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1620, N'Gwanda  - 100561 - Provincial Hospital', N'lab', 52, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1621, N'Gweru  - 100572 - Provincial Hospital', N'lab', 58, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1622, N'Kadoma - 100681 - District Hosp', N'lab', 68, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1623, N'Marondera  - 100903 - Provincial Hospital', N'lab', 27, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1624, N'Masvingo - 100937 - General Hospital', N'lab', 38, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1625, N'Mpilo - 101041 - Central Hospital', N'lab', 1, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1626, N'Mutare - 101165 - Provincial Hospital', N'lab', 9, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1627, N'National Reference Laboratory - 101206 - Laboratory', N'lab', 3, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1628, N'St. Lukes - 101645 - Mission Hospital', N'lab', 47, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1629, N'United Bulawayo Hospital - 101723 - Central Hospital', N'lab', 1, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1630, N'Victoria Falls - 101739 - District Hospital', N'lab', 46, N'', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1631, N'Mutawatawa District Hospital', N'hub', 25, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1632, N'St. Albert''s Mission Hospital', N'hub', 18, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1633, N'St. Michaels Mission Hospital', N'hub', 33, N'TA-SDI', N'');
INSERT INTO dbo.[operations_facility] ([id], [name], [kind], [district_id], [support_type], [site_code]) VALUES (1634, N'St Theresa Hospital', N'hub', 61, N'TA-SDI', N'');

-- operations_pcprofile
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (1, 2);
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (2, 3);
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (3, 4);
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (4, 5);
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (5, 6);
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (6, 7);
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (7, 8);
INSERT INTO dbo.[operations_pcprofile] ([id], [user_id]) VALUES (8, 9);

-- operations_pcprofile_provinces
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (1, 1, 1);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (2, 2, 2);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (3, 2, 3);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (4, 3, 4);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (5, 4, 5);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (6, 4, 6);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (7, 5, 7);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (8, 6, 8);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (9, 7, 9);
INSERT INTO dbo.[operations_pcprofile_provinces] ([id], [pcprofile_id], [province_id]) VALUES (10, 8, 10);

-- operations_province
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (1, N'Mashonaland Central', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (2, N'Matabeleland North', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (3, N'Bulawayo', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (4, N'Manicaland', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (5, N'Mashonaland East', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (6, N'Harare', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (7, N'Midlands', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (8, N'Matabeleland South', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (9, N'Masvingo', N'');
INSERT INTO dbo.[operations_province] ([id], [name], [code]) VALUES (10, N'Mashonaland West', N'');

-- operations_registereddevice
INSERT INTO dbo.[operations_registereddevice] ([id], [device_id], [platform], [user_agent], [last_seen_at], [created_at], [user_id]) VALUES (1, N'9525aea9-d2e6-4807-a5f5-a447a1b00c76', N'web', N'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0', N'2026-04-08 07:29:53.143226', N'2026-04-08 07:03:35.498461', 1);
INSERT INTO dbo.[operations_registereddevice] ([id], [device_id], [platform], [user_agent], [last_seen_at], [created_at], [user_id]) VALUES (2, N'9525aea9-d2e6-4807-a5f5-a447a1b00c76', N'web', N'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0', N'2026-04-08 13:33:52.988189', N'2026-04-08 09:29:26.638956', 10);
INSERT INTO dbo.[operations_registereddevice] ([id], [device_id], [platform], [user_agent], [last_seen_at], [created_at], [user_id]) VALUES (3, N'9525aea9-d2e6-4807-a5f5-a447a1b00c76', N'web', N'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 Edg/146.0.0.0', N'2026-04-08 17:42:13.355568', N'2026-04-08 14:32:44.424699', 291);

-- operations_reportauditlog
INSERT INTO dbo.[operations_reportauditlog] ([id], [action], [payload], [created_at], [actor_id], [report_id]) VALUES (1, N'submit', N'{}', N'2026-04-08 13:34:02.247917', 10, 1);
INSERT INTO dbo.[operations_reportauditlog] ([id], [action], [payload], [created_at], [actor_id], [report_id]) VALUES (2, N'submit', N'{}', N'2026-04-08 17:42:10.291592', 291, 2);

-- operations_riderprofile
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (1, 1, 1, NULL, 10, 3, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (2, 2, 1, NULL, 11, 3, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (3, 3, 1, NULL, 12, 3, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (4, 4, 2, NULL, 13, 3, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (5, 5, 3, NULL, 14, 6, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (6, 6, 3, NULL, 15, 6, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (7, 7, 3, NULL, 16, 6, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (8, 8, 3, NULL, 17, 6, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (9, 9, 4, NULL, 18, 6, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (10, 10, 4, NULL, 19, 6, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (11, 11, 4, NULL, 20, 6, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (12, 12, 5, NULL, 21, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (13, 13, 5, NULL, 22, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (14, 14, 5, NULL, 23, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (15, 15, 5, NULL, 24, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (16, 16, 5, NULL, 25, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (17, 17, 5, NULL, 26, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (18, 18, 6, NULL, 27, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (19, 19, 6, NULL, 28, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (20, 20, 6, NULL, 29, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (21, 21, 6, NULL, 30, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (22, 22, 7, NULL, 31, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (23, 23, 7, NULL, 32, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (24, 24, 7, NULL, 33, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (25, 25, 7, NULL, 34, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (26, 26, 7, NULL, 35, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (27, 27, 7, NULL, 36, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (28, 28, 7, NULL, 37, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (29, 29, 7, NULL, 38, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (30, 30, 8, NULL, 39, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (31, 31, 8, NULL, 40, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (32, 32, 8, NULL, 41, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (33, 33, 8, NULL, 42, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (34, 34, 8, NULL, 43, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (35, 35, 8, NULL, 44, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (36, 36, 8, NULL, 45, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (37, 37, 8, NULL, 46, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (38, 38, 9, NULL, 47, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (39, 39, 9, NULL, 48, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (40, 40, 9, NULL, 49, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (41, 41, 9, NULL, 50, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (42, 42, 9, NULL, 51, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (43, 43, 9, NULL, 52, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (44, 44, 9, NULL, 53, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (45, 45, 9, NULL, 54, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (46, 46, 10, NULL, 55, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (47, 47, 10, NULL, 56, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (48, 48, 10, NULL, 57, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (49, 49, 10, NULL, 58, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (50, 50, 10, NULL, 59, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (51, 51, 10, NULL, 60, 4, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (52, 52, 11, NULL, 61, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (53, 53, 11, NULL, 62, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (54, 54, 11, NULL, 63, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (55, 55, 11, NULL, 64, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (56, 56, 11, NULL, 65, 4, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (57, 57, 12, NULL, 66, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (58, 58, 12, NULL, 67, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (59, 59, 12, NULL, 68, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (60, 60, 12, NULL, 69, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (61, 61, 12, NULL, 70, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (62, 62, 13, NULL, 71, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (63, 63, 13, NULL, 72, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (64, 64, 13, NULL, 73, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (65, 65, 13, NULL, 74, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (66, 66, 14, NULL, 75, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (67, 67, 14, NULL, 76, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (68, 68, 14, NULL, 77, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (69, 69, 14, NULL, 78, 1, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (70, 70, 15, NULL, 79, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (71, 71, 15, NULL, 80, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (72, 72, 15, NULL, 81, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (73, 73, 15, NULL, 82, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (74, 74, 16, NULL, 83, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (75, 75, 16, NULL, 84, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (76, 76, 16, NULL, 85, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (77, 77, 17, NULL, 86, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (78, 78, 17, NULL, 87, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (79, 79, 17, NULL, 88, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (80, 80, 18, NULL, 89, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (81, 81, 18, NULL, 90, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (82, 82, 18, NULL, 91, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (83, 83, 19, NULL, 92, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (84, 84, 19, NULL, 93, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (85, 85, 19, NULL, 94, 1, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (86, 86, 20, NULL, 95, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (87, 87, 20, NULL, 96, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (88, 88, 20, NULL, 97, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (89, 89, 20, NULL, 98, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (90, 90, 20, NULL, 99, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (91, 91, 20, NULL, 100, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (92, 92, 21, NULL, 101, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (93, 93, 21, NULL, 102, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (94, 94, 21, NULL, 103, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (95, 95, 22, NULL, 104, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (96, 96, 22, NULL, 105, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (97, 97, 22, NULL, 106, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (98, 98, 22, NULL, 107, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (99, 99, 22, NULL, 108, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (100, 100, 23, NULL, 109, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (101, 101, 23, NULL, 110, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (102, 102, 23, NULL, 111, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (103, 103, 24, NULL, 112, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (104, 104, 24, NULL, 113, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (105, 105, 24, NULL, 114, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (106, 106, 25, NULL, 115, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (107, 107, 25, NULL, 116, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (108, 108, 25, NULL, 117, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (109, 109, 26, NULL, 118, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (110, 110, 26, NULL, 119, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (111, 111, 26, NULL, 120, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (112, 112, 27, NULL, 121, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (113, 113, 27, NULL, 122, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (114, 114, 27, NULL, 123, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (115, 115, 27, NULL, 124, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (116, 116, 28, NULL, 125, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (117, 117, 28, NULL, 126, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (118, 118, 28, NULL, 127, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (119, 119, 28, NULL, 128, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (120, 120, 25, NULL, 129, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (121, 121, 26, NULL, 130, 5, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (122, 122, 23, NULL, 131, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (123, 123, 23, NULL, 132, 5, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (124, 124, 29, NULL, 133, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (125, 125, 29, NULL, 134, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (126, 126, 29, NULL, 135, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (127, 127, 29, NULL, 136, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (128, 128, 29, NULL, 137, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (129, 129, 29, NULL, 138, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (130, 130, 30, NULL, 139, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (131, 131, 30, NULL, 140, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (132, 132, 30, NULL, 141, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (133, 133, 30, NULL, 142, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (134, 134, 30, NULL, 143, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (135, 135, 30, NULL, 144, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (136, 136, 31, NULL, 145, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (137, 137, 31, NULL, 146, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (138, 138, 31, NULL, 147, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (139, 139, 31, NULL, 148, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (140, 140, 31, NULL, 149, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (141, 141, 32, NULL, 150, 10, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (142, 142, 32, NULL, 151, 10, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (143, 143, 32, NULL, 152, 10, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (144, 144, 33, NULL, 153, 10, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (145, 145, 33, NULL, 154, 10, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (146, 146, 33, NULL, 155, 10, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (147, 147, 33, NULL, 156, 10, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (148, 148, 34, NULL, 157, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (149, 149, 34, NULL, 158, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (150, 150, 34, NULL, 159, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (151, 151, 34, NULL, 160, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (152, 152, 34, NULL, 161, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (153, 153, 34, NULL, 162, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (154, 154, 35, NULL, 163, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (155, 155, 35, NULL, 164, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (156, 156, 35, NULL, 165, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (157, 157, 35, NULL, 166, 10, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (158, 158, 36, NULL, 167, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (159, 159, 37, NULL, 168, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (160, 160, 37, NULL, 169, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (161, 161, 37, NULL, 170, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (162, 162, 37, NULL, 171, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (163, 163, 38, NULL, 172, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (164, 164, 38, NULL, 173, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (165, 165, 38, NULL, 174, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (166, 166, 38, NULL, 175, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (167, 167, 38, NULL, 176, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (168, 168, 38, NULL, 177, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (169, 169, 39, NULL, 178, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (170, 170, 39, NULL, 179, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (171, 171, 40, NULL, 180, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (172, 172, 40, NULL, 181, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (173, 173, 40, NULL, 182, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (174, 174, 40, NULL, 183, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (175, 175, 39, NULL, 184, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (176, 176, 39, NULL, 185, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (177, 177, 41, NULL, 186, 9, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (178, 178, 41, NULL, 187, 9, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (179, 179, 41, NULL, 188, 9, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (180, 180, 41, NULL, 189, 9, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (181, 181, 41, NULL, 190, 9, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (182, 182, 42, NULL, 191, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (183, 183, 42, NULL, 192, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (184, 184, 42, NULL, 193, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (185, 185, 42, NULL, 194, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (186, 186, 42, NULL, 195, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (187, 187, 42, NULL, 196, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (188, 188, 36, NULL, 197, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (189, 189, 36, NULL, 198, 9, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (190, 190, 43, NULL, 199, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (191, 191, 43, NULL, 200, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (192, 192, 43, NULL, 201, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (193, 193, 44, NULL, 202, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (194, 194, 44, NULL, 203, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (195, 195, 44, NULL, 204, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (196, 196, 45, NULL, 205, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (197, 197, 45, NULL, 206, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (198, 198, 46, NULL, 207, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (199, 199, 46, NULL, 208, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (200, 200, 46, NULL, 209, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (201, 201, 46, NULL, 210, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (202, 202, 46, NULL, 211, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (203, 203, 46, NULL, 212, 2, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (204, 204, 47, NULL, 213, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (205, 205, 47, NULL, 214, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (206, 206, 47, NULL, 215, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (207, 207, 48, NULL, 216, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (208, 208, 48, NULL, 217, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (209, 209, 48, NULL, 218, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (210, 210, 48, NULL, 219, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (211, 211, 49, NULL, 220, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (212, 212, 49, NULL, 221, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (213, 213, 49, NULL, 222, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (214, 214, 49, NULL, 223, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (215, 215, 43, NULL, 224, 2, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (216, 216, 50, NULL, 225, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (217, 217, 50, NULL, 226, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (218, 218, 50, NULL, 227, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (219, 219, 51, NULL, 228, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (220, 220, 51, NULL, 229, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (221, 221, 51, NULL, 230, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (222, 222, 51, NULL, 231, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (223, 223, 52, NULL, 232, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (224, 224, 52, NULL, 233, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (225, 225, 52, NULL, 234, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (226, 226, 52, NULL, 235, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (227, 227, 53, NULL, 236, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (228, 228, 53, NULL, 237, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (229, 229, 53, NULL, 238, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (230, 230, 53, NULL, 239, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (231, 231, 54, NULL, 240, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (232, 232, 54, NULL, 241, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (233, 233, 54, NULL, 242, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (234, 234, 55, NULL, 243, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (235, 235, 55, NULL, 244, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (236, 236, 55, NULL, 245, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (237, 237, 55, NULL, 246, 8, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (238, 238, 56, NULL, 247, 8, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (239, 239, 56, NULL, 248, 8, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (240, 240, 56, NULL, 249, 8, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (241, 241, 57, NULL, 250, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (242, 242, 57, NULL, 251, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (243, 243, 57, NULL, 252, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (244, 244, 58, NULL, 253, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (245, 245, 58, NULL, 254, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (246, 246, 58, NULL, 255, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (247, 247, 58, NULL, 256, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (248, 248, 59, NULL, 257, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (249, 249, 59, NULL, 258, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (250, 250, 59, NULL, 259, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (251, 251, 59, NULL, 260, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (252, 252, 59, NULL, 261, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (253, 253, 59, NULL, 262, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (254, 254, 60, NULL, 263, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (255, 255, 60, NULL, 264, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (256, 256, 60, NULL, 265, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (257, 257, 60, NULL, 266, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (258, 258, 60, NULL, 267, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (259, 259, 61, NULL, 268, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (260, 260, 61, NULL, 269, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (261, 261, 62, NULL, 270, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (262, 262, 62, NULL, 271, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (263, 263, 62, NULL, 272, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (264, 264, 62, NULL, 273, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (265, 265, 63, NULL, 274, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (266, 266, 63, NULL, 275, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (267, 267, 63, NULL, 276, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (268, 268, 63, NULL, 277, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (269, 269, 63, NULL, 278, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (270, 270, 64, NULL, 279, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (271, 271, 64, NULL, 280, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (272, 272, 64, NULL, 281, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (273, 273, 64, NULL, 282, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (274, 274, 64, NULL, 283, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (275, 275, 61, NULL, 284, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (276, 276, 61, NULL, 285, 7, N'TA-SDI', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (277, 277, 57, NULL, 286, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (278, 278, 57, NULL, 287, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (279, 279, 57, NULL, 288, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (280, 280, 60, NULL, 289, 7, N'DSD', NULL);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (281, NULL, NULL, NULL, 290, 7, N'', 1);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (282, NULL, NULL, NULL, 291, 2, N'', 2);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (283, NULL, NULL, NULL, 292, 5, N'', 3);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (284, NULL, NULL, NULL, 293, 8, N'', 4);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (285, NULL, NULL, NULL, 294, 10, N'', 5);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (286, NULL, NULL, NULL, 295, 9, N'', 6);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (287, NULL, NULL, NULL, 296, 4, N'', 7);
INSERT INTO dbo.[operations_riderprofile] ([id], [bike_id], [district_id], [facility_id], [user_id], [province_id], [support_type], [car_id]) VALUES (288, NULL, NULL, NULL, 297, 1, N'', 8);

-- operations_ridertripentry
INSERT INTO dbo.[operations_ridertripentry] ([id], [row_uuid], [sequence], [entry_date], [vl_blood_plasma], [vl_dbs], [eid_blood], [eid_dbs], [sputum], [sputum_culture_dr], [hpv], [specimens_other_specify], [results_vl_blood_plasma], [results_vl_dbs], [results_eid_blood], [results_eid_dbs], [results_sputum], [results_sputum_culture_dr], [results_hpv], [results_other_specify], [fuel_allocated], [fuel_used], [distance_travelled], [created_at], [updated_at], [report_id], [destination_facility_id], [origin_facility_id], [route_kind], [visit_purpose], [transport_kind]) VALUES (1, N'645f856a43bc4ecd9a47999d26a0e7a7', 1, N'2026-04-08', 2, 3, 1, 0, 0, 0, 0, N'10fbc', 2, 0, 0, 0, 0, 0, 0, N'', 22, 22, 224, N'2026-04-08 12:22:10.976261', N'2026-04-08 12:22:10.976308', 1, 484, 483, N'facility_to_facility', N'sample_collection', N'legacy');
INSERT INTO dbo.[operations_ridertripentry] ([id], [row_uuid], [sequence], [entry_date], [vl_blood_plasma], [vl_dbs], [eid_blood], [eid_dbs], [sputum], [sputum_culture_dr], [hpv], [specimens_other_specify], [results_vl_blood_plasma], [results_vl_dbs], [results_eid_blood], [results_eid_dbs], [results_sputum], [results_sputum_culture_dr], [results_hpv], [results_other_specify], [fuel_allocated], [fuel_used], [distance_travelled], [created_at], [updated_at], [report_id], [destination_facility_id], [origin_facility_id], [route_kind], [visit_purpose], [transport_kind]) VALUES (2, N'7018aec1f07745999796caa154fae09b', 1, N'2026-04-08', 2, 2, 0, 0, 0, 0, 0, N'', 0, 4, 0, 0, 0, 0, 0, N'', 0, 0, 0, N'2026-04-08 17:41:49.158255', N'2026-04-08 17:41:49.158287', 2, 1628, 1260, N'facility_to_lab', N'sample_collection', N'relayed');
INSERT INTO dbo.[operations_ridertripentry] ([id], [row_uuid], [sequence], [entry_date], [vl_blood_plasma], [vl_dbs], [eid_blood], [eid_dbs], [sputum], [sputum_culture_dr], [hpv], [specimens_other_specify], [results_vl_blood_plasma], [results_vl_dbs], [results_eid_blood], [results_eid_dbs], [results_sputum], [results_sputum_culture_dr], [results_hpv], [results_other_specify], [fuel_allocated], [fuel_used], [distance_travelled], [created_at], [updated_at], [report_id], [destination_facility_id], [origin_facility_id], [route_kind], [visit_purpose], [transport_kind]) VALUES (3, N'933b92980c354fbdb1405b9115a03a74', 2, N'2026-04-08', 4, 0, 0, 0, 0, 0, 0, N'', 0, 0, 0, 0, 0, 0, 4, N'', 0, 0, 0, N'2026-04-08 17:41:49.160299', N'2026-04-08 17:41:49.160328', 2, 1354, 1628, N'lab_to_facility', N'sample_collection', N'first_transport');

-- operations_riderweeklyreport
INSERT INTO dbo.[operations_riderweeklyreport] ([id], [client_uuid], [week_start], [status], [title], [notes], [samples_collected], [extra_data], [submitted_at], [review_started_at], [reviewed_at], [pc_notes], [created_at], [updated_at], [reviewed_by_id], [rider_id], [bike_id], [scheduled_visits], [average_datalogger_temperature], [car_id]) VALUES (1, NULL, N'2026-04-06', N'submitted', N'Bulawayo / Bulawayo', N'', 6, N'{}', N'2026-04-08 13:34:02.245366', NULL, NULL, N'', N'2026-04-08 12:22:10.971453', N'2026-04-08 13:34:02.245597', NULL, 10, 3, NULL, NULL, NULL);
INSERT INTO dbo.[operations_riderweeklyreport] ([id], [client_uuid], [week_start], [status], [title], [notes], [samples_collected], [extra_data], [submitted_at], [review_started_at], [reviewed_at], [pc_notes], [created_at], [updated_at], [reviewed_by_id], [rider_id], [bike_id], [scheduled_visits], [average_datalogger_temperature], [car_id]) VALUES (2, NULL, N'2026-04-06', N'submitted', N'', N'', 8, N'{}', N'2026-04-08 17:42:10.288878', NULL, NULL, N'', N'2026-04-08 17:41:49.155589', N'2026-04-08 17:42:10.289038', NULL, 291, NULL, NULL, 12, 2);

-- operations_userprofile
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (1, N'rider', 1);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (2, N'pc', 2);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (3, N'pc', 3);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (4, N'pc', 4);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (5, N'pc', 5);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (6, N'pc', 6);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (7, N'pc', 7);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (8, N'pc', 8);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (9, N'pc', 9);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (10, N'rider', 10);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (11, N'rider', 11);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (12, N'rider', 12);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (13, N'rider', 13);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (14, N'rider', 14);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (15, N'rider', 15);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (16, N'rider', 16);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (17, N'rider', 17);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (18, N'rider', 18);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (19, N'rider', 19);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (20, N'rider', 20);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (21, N'rider', 21);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (22, N'rider', 22);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (23, N'rider', 23);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (24, N'rider', 24);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (25, N'rider', 25);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (26, N'rider', 26);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (27, N'rider', 27);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (28, N'rider', 28);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (29, N'rider', 29);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (30, N'rider', 30);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (31, N'rider', 31);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (32, N'rider', 32);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (33, N'rider', 33);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (34, N'rider', 34);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (35, N'rider', 35);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (36, N'rider', 36);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (37, N'rider', 37);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (38, N'rider', 38);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (39, N'rider', 39);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (40, N'rider', 40);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (41, N'rider', 41);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (42, N'rider', 42);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (43, N'rider', 43);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (44, N'rider', 44);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (45, N'rider', 45);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (46, N'rider', 46);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (47, N'rider', 47);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (48, N'rider', 48);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (49, N'rider', 49);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (50, N'rider', 50);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (51, N'rider', 51);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (52, N'rider', 52);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (53, N'rider', 53);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (54, N'rider', 54);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (55, N'rider', 55);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (56, N'rider', 56);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (57, N'rider', 57);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (58, N'rider', 58);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (59, N'rider', 59);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (60, N'rider', 60);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (61, N'rider', 61);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (62, N'rider', 62);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (63, N'rider', 63);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (64, N'rider', 64);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (65, N'rider', 65);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (66, N'rider', 66);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (67, N'rider', 67);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (68, N'rider', 68);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (69, N'rider', 69);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (70, N'rider', 70);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (71, N'rider', 71);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (72, N'rider', 72);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (73, N'rider', 73);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (74, N'rider', 74);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (75, N'rider', 75);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (76, N'rider', 76);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (77, N'rider', 77);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (78, N'rider', 78);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (79, N'rider', 79);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (80, N'rider', 80);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (81, N'rider', 81);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (82, N'rider', 82);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (83, N'rider', 83);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (84, N'rider', 84);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (85, N'rider', 85);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (86, N'rider', 86);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (87, N'rider', 87);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (88, N'rider', 88);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (89, N'rider', 89);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (90, N'rider', 90);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (91, N'rider', 91);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (92, N'rider', 92);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (93, N'rider', 93);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (94, N'rider', 94);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (95, N'rider', 95);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (96, N'rider', 96);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (97, N'rider', 97);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (98, N'rider', 98);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (99, N'rider', 99);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (100, N'rider', 100);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (101, N'rider', 101);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (102, N'rider', 102);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (103, N'rider', 103);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (104, N'rider', 104);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (105, N'rider', 105);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (106, N'rider', 106);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (107, N'rider', 107);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (108, N'rider', 108);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (109, N'rider', 109);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (110, N'rider', 110);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (111, N'rider', 111);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (112, N'rider', 112);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (113, N'rider', 113);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (114, N'rider', 114);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (115, N'rider', 115);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (116, N'rider', 116);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (117, N'rider', 117);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (118, N'rider', 118);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (119, N'rider', 119);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (120, N'rider', 120);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (121, N'rider', 121);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (122, N'rider', 122);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (123, N'rider', 123);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (124, N'rider', 124);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (125, N'rider', 125);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (126, N'rider', 126);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (127, N'rider', 127);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (128, N'rider', 128);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (129, N'rider', 129);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (130, N'rider', 130);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (131, N'rider', 131);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (132, N'rider', 132);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (133, N'rider', 133);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (134, N'rider', 134);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (135, N'rider', 135);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (136, N'rider', 136);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (137, N'rider', 137);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (138, N'rider', 138);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (139, N'rider', 139);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (140, N'rider', 140);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (141, N'rider', 141);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (142, N'rider', 142);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (143, N'rider', 143);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (144, N'rider', 144);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (145, N'rider', 145);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (146, N'rider', 146);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (147, N'rider', 147);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (148, N'rider', 148);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (149, N'rider', 149);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (150, N'rider', 150);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (151, N'rider', 151);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (152, N'rider', 152);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (153, N'rider', 153);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (154, N'rider', 154);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (155, N'rider', 155);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (156, N'rider', 156);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (157, N'rider', 157);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (158, N'rider', 158);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (159, N'rider', 159);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (160, N'rider', 160);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (161, N'rider', 161);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (162, N'rider', 162);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (163, N'rider', 163);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (164, N'rider', 164);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (165, N'rider', 165);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (166, N'rider', 166);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (167, N'rider', 167);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (168, N'rider', 168);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (169, N'rider', 169);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (170, N'rider', 170);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (171, N'rider', 171);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (172, N'rider', 172);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (173, N'rider', 173);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (174, N'rider', 174);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (175, N'rider', 175);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (176, N'rider', 176);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (177, N'rider', 177);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (178, N'rider', 178);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (179, N'rider', 179);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (180, N'rider', 180);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (181, N'rider', 181);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (182, N'rider', 182);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (183, N'rider', 183);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (184, N'rider', 184);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (185, N'rider', 185);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (186, N'rider', 186);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (187, N'rider', 187);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (188, N'rider', 188);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (189, N'rider', 189);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (190, N'rider', 190);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (191, N'rider', 191);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (192, N'rider', 192);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (193, N'rider', 193);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (194, N'rider', 194);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (195, N'rider', 195);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (196, N'rider', 196);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (197, N'rider', 197);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (198, N'rider', 198);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (199, N'rider', 199);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (200, N'rider', 200);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (201, N'rider', 201);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (202, N'rider', 202);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (203, N'rider', 203);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (204, N'rider', 204);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (205, N'rider', 205);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (206, N'rider', 206);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (207, N'rider', 207);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (208, N'rider', 208);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (209, N'rider', 209);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (210, N'rider', 210);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (211, N'rider', 211);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (212, N'rider', 212);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (213, N'rider', 213);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (214, N'rider', 214);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (215, N'rider', 215);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (216, N'rider', 216);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (217, N'rider', 217);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (218, N'rider', 218);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (219, N'rider', 219);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (220, N'rider', 220);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (221, N'rider', 221);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (222, N'rider', 222);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (223, N'rider', 223);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (224, N'rider', 224);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (225, N'rider', 225);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (226, N'rider', 226);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (227, N'rider', 227);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (228, N'rider', 228);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (229, N'rider', 229);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (230, N'rider', 230);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (231, N'rider', 231);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (232, N'rider', 232);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (233, N'rider', 233);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (234, N'rider', 234);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (235, N'rider', 235);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (236, N'rider', 236);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (237, N'rider', 237);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (238, N'rider', 238);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (239, N'rider', 239);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (240, N'rider', 240);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (241, N'rider', 241);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (242, N'rider', 242);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (243, N'rider', 243);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (244, N'rider', 244);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (245, N'rider', 245);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (246, N'rider', 246);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (247, N'rider', 247);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (248, N'rider', 248);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (249, N'rider', 249);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (250, N'rider', 250);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (251, N'rider', 251);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (252, N'rider', 252);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (253, N'rider', 253);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (254, N'rider', 254);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (255, N'rider', 255);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (256, N'rider', 256);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (257, N'rider', 257);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (258, N'rider', 258);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (259, N'rider', 259);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (260, N'rider', 260);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (261, N'rider', 261);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (262, N'rider', 262);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (263, N'rider', 263);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (264, N'rider', 264);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (265, N'rider', 265);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (266, N'rider', 266);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (267, N'rider', 267);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (268, N'rider', 268);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (269, N'rider', 269);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (270, N'rider', 270);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (271, N'rider', 271);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (272, N'rider', 272);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (273, N'rider', 273);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (274, N'rider', 274);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (275, N'rider', 275);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (276, N'rider', 276);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (277, N'rider', 277);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (278, N'rider', 278);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (279, N'rider', 279);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (280, N'rider', 280);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (281, N'rider', 281);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (282, N'rider', 282);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (283, N'rider', 283);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (284, N'rider', 284);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (285, N'rider', 285);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (286, N'rider', 286);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (287, N'rider', 287);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (288, N'rider', 288);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (289, N'rider', 289);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (290, N'driver', 290);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (291, N'driver', 291);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (292, N'driver', 292);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (293, N'driver', 293);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (294, N'driver', 294);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (295, N'driver', 295);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (296, N'driver', 296);
INSERT INTO dbo.[operations_userprofile] ([id], [role], [user_id]) VALUES (297, N'driver', 297);

COMMIT TRANSACTION;