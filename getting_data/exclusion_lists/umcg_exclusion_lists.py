
exclude_subject_ids_treatment = [
    'M-083_83-0',   # TURP
    'M-285_286-0',  # TURP
    'M-449_465-0',  # TURP
    'U-125_706-0',  # TURP
    'M-264_265-0',  # catheter
    'M-266_267-0',  # catheter
    'M-513_560-0',  # indication of TURP 
    'M-130_130-0',  # indication of TURP
    'M-020_20-0',   # TURP
    'M-304_305-0',  # TURP
    'M-340_341-0',  # TURP
    'M-357_358-0',  # TURP
    'M-442_458-0',  # TURP
    'M-517_564-0',  # TURP
    'U-016_449-0',  # TURP
    'U-101_682-0',  # TURP
    'U-126_707-0',  # TURP
    'U-166_747-0',  # TURP
    'U-179_760-0',  # TURP
    'U-352_933-0',  # TURP
    'M-268_269-0',  # TURP
]

exclude_subject_ids_gleason_3_4_and_up = [
    'M-055_55-1',   # prior ISUP>1 finding
    'M-065_65-0',   # prior ISUP>1 finding
    'M-068_68-0',   # prior ISUP>1 finding
    'M-107_107-0',  # prior ISUP>1 finding
    'M-118_118-0',  # prior ISUP>1 finding
    'M-127_127-1',  # prior ISUP>1 finding
    'M-128_128-0',  # prior ISUP>1 finding
    'M-142_142-0',  # prior ISUP>1 finding
    'M-143_143-0',  # prior ISUP>1 finding
    'M-149_149-0',  # prior ISUP>1 finding
    'M-158_158-0',  # prior ISUP>1 finding
    'M-306_307-0',  # prior ISUP>1 finding
    'M-345_346-0',  # prior ISUP>1 finding
    'M-375_376-0',  # prior ISUP>1 finding
    'M-375_376-1',  # prior ISUP>1 finding
    'M-402_403-0',  # prior ISUP>1 finding
    'M-422_432-0',  # prior ISUP>1 finding
    'M-491_526-0',  # prior ISUP>1 finding
    'M-496_536-0',  # prior ISUP>1 finding
    'M-511_558-1',  # prior ISUP>1 finding
    'M-511_558-2',  # prior ISUP>1 finding
    'M-515_562-0',  # prior ISUP>1 finding
    'U-082_608-1',  # prior ISUP>1 finding
    'M-088_88_1',   # prior ISUP>1 finding  
    'U-017_483-0',  # prior ISUP>1 finding  
]

exclude_subject_ids_scan_quality = [
    'M-181_182-0',  # hip prostheses
    'M-182_183-0',  # hip prostheses
    'M-182_183-1',  # hip prostheses
    'M-339_340-0',  # hip prostheses
    'U-356_937-0',  # hip prostheses + duplicate w/ U-346_927-0 yet discordant findings
    'U-346_927-0'   # hip prostheses + duplicate w/ U-356_937-0 yet discordant findings
    'U-198_779-0',  # warping
    'M-147_147-0',  # double hip protheses + T2W significant movement
    'M-166_167-0',  # PI-QUAL v2 < 5; heavy movement T2w, heavy warping distortions DWI
    'M-526_573-0',  # PI-QUAL v2 < 5; moderate movement T2w
    'M-449_465-0',  # Hip prothesis, low quality DWI
    'M-086_86-0',   # severe rectal warping
    'M-147_147-0',  # double hip protheses + T2W significant movement
    'M-513_560-0',  # T2w significant movement
    'U-346_927-0',  # double hip prostheses
    'M-468_487-0',  # hip prostheses
    'M-468_487-1',  # hip prostheses
    'M-428_441-0',  # hip prostheses
    'M-349_350-1',  # hip prostheses
    'M-349_350-2',  # hip prostheses
    'U-092_673-0',  # ERC
    'U-185_766-0',  # ERC
]

exclude_subject_list_no_radiology_report = [
]

exclude_subject_list_inconclusive_radiology_report = [
]

exclude_subject_ids_no_detection_study = [
]

exclude_subject_ids_misc = [
    'M-305_306-0',  # missing PI-RADS score
    'M-578_666-0',  # missing PI-RADS score
    'U-072_598-0',  # missing PI-RADS score
    'U-029_512-0',  # missing PI-RADS score
    'M-087_87-0',   # missing HBV acquisition
    'M-124_124-0',  # missing HBV acquisition
    'M-124_124-1',  # missing HBV acquisition
    'M-249_250-0',  # missing HBV acquisition
    'M-477_503-0',  # missing ADC acquisition
    'M-556_644-0',  # missing ADC acquisition
    'U-187_768-0',  # missing HBV acquisition
    'U-203_784-0',  # missing HBV acquisition
    'U-364_945-0',  # missing HBV acquisition
    'U-313_894-0',  # missing HBV acquisition
    'U-082_608-0',  # missing HBV acquisition
    'U-313_894-0',  # missing HBV acquisition
    'U-035_525-0',  # missing axial T2W
    'U-268_849-0',  # zoomit DWI sequence
    'M-365_366-0',  # inconsistent MRI dates; marksheet says 2016, dcm folder is for 2018
    'M-492_528-0',  # inconsistent MRI dates; marksheet says 2017, dcm folder is for 2018 
    'U-220_801-0',  # scans completely out-of-plane
    'M-575_663-0',  # incorrect image orientation
    'U-306_887-0',  # incorrect image orientation
]

exclusion_list_default = (
    exclude_subject_ids_treatment
    + exclude_subject_ids_gleason_3_4_and_up
    + exclude_subject_ids_scan_quality
    + exclude_subject_list_no_radiology_report
    + exclude_subject_list_inconclusive_radiology_report
    + exclude_subject_ids_no_detection_study
)

exclusion_list_picai = (
    exclusion_list_default
    + exclude_subject_ids_misc
)
