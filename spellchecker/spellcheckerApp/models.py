# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CrawlerIndexConfigs(models.Model):
    crawler_index_config_id = models.BigAutoField(primary_key=True)
    batch_size = models.IntegerField(blank=True, null=True)
    canonical_link_detector = models.TextField(blank=True, null=True)  # This field type is a guess.
    max_depth = models.IntegerField(blank=True, null=True)
    max_documents = models.IntegerField(blank=True, null=True)
    max_retries = models.IntegerField(blank=True, null=True)
    num_threads = models.IntegerField(blank=True, null=True)
    retry_delay = models.IntegerField(blank=True, null=True)
    robots_txt = models.TextField(blank=True, null=True)  # This field type is a guess.
    sitemap_resolver = models.TextField(blank=True, null=True)  # This field type is a guess.
    solr_url = models.CharField(max_length=255, blank=True, null=True)
    stay_on_domain = models.TextField(blank=True, null=True)  # This field type is a guess.
    stay_on_port = models.TextField(blank=True, null=True)  # This field type is a guess.
    stay_on_protocol = models.TextField(blank=True, null=True)  # This field type is a guess.
    crawler = models.OneToOneField('Crawlers', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawler_index_configs'


class Crawlers(models.Model):
    crawler_id = models.CharField(primary_key=True, max_length=255)
    active = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.DateTimeField(blank=True, null=True)
    end_crawl_date = models.DateTimeField(blank=True, null=True)
    external_ip = models.CharField(max_length=255, blank=True, null=True)
    initial_crawl_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    name_pods = models.CharField(max_length=255, blank=True, null=True)
    namespace = models.CharField(max_length=255, blank=True, null=True)
    path_solr = models.CharField(max_length=255, blank=True, null=True)
    path_solr_features = models.CharField(max_length=255, blank=True, null=True)
    path_solr_main = models.CharField(max_length=255, blank=True, null=True)
    path_solr_signals = models.CharField(max_length=255, blank=True, null=True)
    port_nginx = models.CharField(max_length=255, blank=True, null=True)
    port_tomcat = models.CharField(max_length=255, blank=True, null=True)
    status = models.BigIntegerField(blank=True, null=True)
    status_message = models.CharField(max_length=255, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    organization = models.OneToOneField('Organizations', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'crawlers'


class CustomContentJoinDropdown(models.Model):
    custom_content = models.ForeignKey('ResultsSectionCustomContentConfigs', models.DO_NOTHING)
    custom_content_dropdown = models.OneToOneField('ResultsSectionCustomContentDropdownConfigs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'custom_content_join_dropdown'
        unique_together = (('custom_content', 'custom_content_dropdown'),)


class DateBucketFilterConfigs(models.Model):
    date_bucket_filter_id = models.BigAutoField(primary_key=True)
    searchable_granularity = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'date_bucket_filter_configs'


class DateBucketItemFilterConfigs(models.Model):
    date_bucket_item_filter_id = models.BigAutoField(primary_key=True)
    data_field_granularity = models.CharField(max_length=255, blank=True, null=True)
    filter_field_granularity = models.CharField(max_length=255, blank=True, null=True)
    limit_granularity = models.CharField(max_length=255, blank=True, null=True)
    order_granularity = models.CharField(max_length=255, blank=True, null=True)
    sort_granularity = models.CharField(max_length=255, blank=True, null=True)
    sortable_granularity = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'date_bucket_item_filter_configs'


class DateBucketJoinDateBucketItemFiltersConfigs(models.Model):
    date_bucket_filter = models.ForeignKey(DateBucketFilterConfigs, models.DO_NOTHING)
    date_bucket_item_filter = models.OneToOneField(DateBucketItemFilterConfigs, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'date_bucket_join_date_bucket_item_filters_configs'
        unique_together = (('date_bucket_filter', 'date_bucket_item_filter'),)


class DateRangeFilterConfigs(models.Model):
    date_range_filter_id = models.BigAutoField(primary_key=True)
    data_field_range = models.CharField(max_length=255, blank=True, null=True)
    filter_field_range = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'date_range_filter_configs'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FooterJoinFooterItem(models.Model):
    footer = models.ForeignKey('SearchEngineFooterConfigs', models.DO_NOTHING)
    footer_item = models.OneToOneField('SearchEngineFooterItemConfigs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'footer_join_footer_item'
        unique_together = (('footer', 'footer_item'),)


class MatchFilterConfigs(models.Model):
    match_filter_id = models.BigAutoField(primary_key=True)
    data_field = models.CharField(max_length=255, blank=True, null=True)
    filter_field = models.CharField(max_length=255, blank=True, null=True)
    limit_filter = models.IntegerField(blank=True, null=True)
    omit_values = models.CharField(max_length=255, blank=True, null=True)
    order_filter = models.CharField(max_length=255, blank=True, null=True)
    searchable = models.TextField()  # This field type is a guess.
    sort_filter = models.CharField(max_length=255, blank=True, null=True)
    sortable = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'match_filter_configs'


class Monitors(models.Model):
    monitor_job_id = models.BigAutoField(primary_key=True)
    avg_throughput = models.FloatField(blank=True, null=True)
    document_queued = models.BigIntegerField(blank=True, null=True)
    duration_job = models.CharField(max_length=255, blank=True, null=True)
    initial_job_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    note_job = models.CharField(max_length=255, blank=True, null=True)
    status_job = models.BigIntegerField(blank=True, null=True)
    total_processed = models.BigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'monitors'


class NavigateFiltersConfigs(models.Model):
    navigate_filter_id = models.BigIntegerField(primary_key=True)
    has_title = models.TextField(blank=True, null=True)  # This field type is a guess.
    initial_collapse_state = models.TextField(blank=True, null=True)  # This field type is a guess.
    collapsable = models.TextField(blank=True, null=True)  # This field type is a guess.
    position = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    type_filter = models.CharField(max_length=255, blank=True, null=True)
    date_bucket_filter = models.OneToOneField(DateBucketFilterConfigs, models.DO_NOTHING, blank=True, null=True)
    date_range_filter = models.OneToOneField(DateRangeFilterConfigs, models.DO_NOTHING, blank=True, null=True)
    match_filter = models.OneToOneField(MatchFilterConfigs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'navigate_filters_configs'


class NavigateJoinNavigateFiltersConfigs(models.Model):
    navigate = models.ForeignKey('SearchEngineNavigateConfigs', models.DO_NOTHING)
    navigate_filter = models.OneToOneField(NavigateFiltersConfigs, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'navigate_join_navigate_filters_configs'
        unique_together = (('navigate', 'navigate_filter'),)


class OneboxConfigJoinCrossSearchConfigs(models.Model):
    cross_search_configs = models.OneToOneField('OneboxCrossSearchConfigs', models.DO_NOTHING, blank=True, null=True)
    onebox_config = models.OneToOneField('SearchEngineOneboxConfigs', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'onebox_config_join_cross_search_configs'
        unique_together = (('onebox_config', 'cross_search_configs'),)


class OneboxConfigJoinFaqConfigs(models.Model):
    faq_configs = models.OneToOneField('OneboxFaqConfigs', models.DO_NOTHING, blank=True, null=True)
    onebox_config = models.OneToOneField('SearchEngineOneboxConfigs', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'onebox_config_join_faq_configs'
        unique_together = (('onebox_config', 'faq_configs'),)


class OneboxConfigJoinLlmRagConfigs(models.Model):
    llm_rag_configs = models.OneToOneField('OneboxLlmRagConfigs', models.DO_NOTHING, blank=True, null=True)
    onebox_config = models.OneToOneField('SearchEngineOneboxConfigs', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'onebox_config_join_llm_rag_configs'
        unique_together = (('onebox_config', 'llm_rag_configs'),)


class OneboxCrossSearchConfigs(models.Model):
    cross_search_configs_id = models.BigAutoField(primary_key=True)
    enable_relevance = models.TextField(blank=True, null=True)  # This field type is a guess.
    search_engine_path = models.CharField(max_length=255, blank=True, null=True)
    show_fields = models.CharField(max_length=255, blank=True, null=True)
    triggers = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'onebox_cross_search_configs'


class OneboxFaqConfigs(models.Model):
    faq_configs_id = models.BigAutoField(primary_key=True)
    enable_prediction = models.TextField(blank=True, null=True)  # This field type is a guess.
    path_service = models.CharField(max_length=255, blank=True, null=True)
    path_service_faq = models.CharField(max_length=255, blank=True, null=True)
    prediction_path_service = models.CharField(max_length=255, blank=True, null=True)
    real_query = models.CharField(max_length=255, blank=True, null=True)
    triggers = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'onebox_faq_configs'


class OneboxLlmRagConfigs(models.Model):
    llm_rag_configs_id = models.BigAutoField(primary_key=True)
    application_id = models.CharField(max_length=255, blank=True, null=True)
    organization_id = models.CharField(max_length=255, blank=True, null=True)
    path_service = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'onebox_llm_rag_configs'


class Organizations(models.Model):
    organization_id = models.BigAutoField(primary_key=True)
    active = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'organizations'


class OrganizationsJoinSearchEngineConfig(models.Model):
    organization = models.ForeignKey(Organizations, models.DO_NOTHING)
    search_engine_config = models.OneToOneField('SearchEngineConfigs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'organizations_join_search_engine_config'
        unique_together = (('organization', 'search_engine_config'),)


class ResultSectionJoinCustomContent(models.Model):
    results_section_config = models.ForeignKey('SearchEngineResultsSectionConfigs', models.DO_NOTHING)
    custom_content = models.OneToOneField('ResultsSectionCustomContentConfigs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'result_section_join_custom_content'
        unique_together = (('results_section_config', 'custom_content'),)


class ResultSectionJoinStyleConfigs(models.Model):
    results_section_config = models.ForeignKey('SearchEngineResultsSectionConfigs', models.DO_NOTHING)
    style_config = models.OneToOneField('StyleConfigs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'result_section_join_style_configs'
        unique_together = (('results_section_config', 'style_config'),)


class ResultsSectionCustomContentConfigs(models.Model):
    custom_content_id = models.BigAutoField(primary_key=True)
    field_data = models.CharField(max_length=255, blank=True, null=True)
    field_link = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    separator_list = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'results_section_custom_content_configs'


class ResultsSectionCustomContentDropdownConfigs(models.Model):
    custom_content_dropdown_id = models.BigAutoField(primary_key=True)
    field_data = models.CharField(max_length=255, blank=True, null=True)
    field_link = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'results_section_custom_content_dropdown_configs'


class Roles(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class SearchEngineAuthenticationConfigs(models.Model):
    authentication_id = models.BigAutoField(primary_key=True)
    path_service = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_authentication_configs'


class SearchEngineConfigJoinLinkSectionItemConfig(models.Model):
    search_engine_config = models.ForeignKey('SearchEngineConfigs', models.DO_NOTHING)
    link_section = models.OneToOneField('SearchEngineLinkSectionItemConfigs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'search_engine_config_join_link_section_item_config'
        unique_together = (('search_engine_config', 'link_section'),)


class SearchEngineConfigJoinOneboxs(models.Model):
    search_engine_config = models.ForeignKey('SearchEngineConfigs', models.DO_NOTHING)
    onebox_config = models.OneToOneField('SearchEngineOneboxConfigs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'search_engine_config_join_oneboxs'
        unique_together = (('search_engine_config', 'onebox_config'),)


class SearchEngineConfigJoinSpellchecker(models.Model):
    spellchecker = models.OneToOneField('SearchEngineSpellcheckerConfigs', models.DO_NOTHING, blank=True, null=True)
    searchbox = models.OneToOneField('SearchEngineSearchboxConfigs', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'search_engine_config_join_spellchecker'
        unique_together = (('searchbox', 'spellchecker'),)


class SearchEngineConfigJoinSuggestion(models.Model):
    suggestion = models.OneToOneField('SearchEngineSuggestionConfigs', models.DO_NOTHING, blank=True, null=True)
    searchbox = models.OneToOneField('SearchEngineSearchboxConfigs', models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'search_engine_config_join_suggestion'
        unique_together = (('searchbox', 'suggestion'),)


class SearchEngineConfigs(models.Model):
    search_engine_config_id = models.BigAutoField(primary_key=True)
    has_filters = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_footer = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_header = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_link_section = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_oneboxes = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_results_section = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_results_summary_section = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_search_bar = models.TextField(blank=True, null=True)  # This field type is a guess.
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_configs'


class SearchEngineFooterConfigs(models.Model):
    footer_id = models.BigAutoField(primary_key=True)
    footer_img_center = models.TextField(blank=True, null=True)
    footer_img_left = models.TextField(blank=True, null=True)
    footer_img_right = models.TextField(blank=True, null=True)
    has_footer_center = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_footer_left = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_footer_right = models.TextField(blank=True, null=True)  # This field type is a guess.
    search_engine_config = models.OneToOneField(SearchEngineConfigs, models.DO_NOTHING, blank=True, null=True)
    style_config = models.OneToOneField('StyleConfigs', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_footer_configs'


class SearchEngineFooterItemConfigs(models.Model):
    footer_item_id = models.BigAutoField(primary_key=True)
    field_link = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_footer_item_configs'


class SearchEngineHeaderConfigs(models.Model):
    header_id = models.BigAutoField(primary_key=True)
    header_img_center_url = models.TextField(blank=True, null=True)
    header_img_left_url = models.TextField(blank=True, null=True)
    header_img_right_url = models.TextField(blank=True, null=True)
    header_title = models.CharField(max_length=255, blank=True, null=True)
    search_engine_config = models.OneToOneField(SearchEngineConfigs, models.DO_NOTHING, blank=True, null=True)
    style_config = models.OneToOneField('StyleConfigs', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_header_configs'


class SearchEngineIndexerConfigs(models.Model):
    id = models.BigAutoField(primary_key=True)
    core = models.CharField(max_length=255, blank=True, null=True)
    core_features = models.CharField(max_length=255, blank=True, null=True)
    core_signals = models.CharField(max_length=255, blank=True, null=True)
    core_signals_spell = models.CharField(max_length=255, blank=True, null=True)
    date_boost = models.CharField(max_length=255, blank=True, null=True)
    enable_group = models.TextField(blank=True, null=True)  # This field type is a guess.
    enable_ltr = models.TextField(blank=True, null=True)  # This field type is a guess.
    field_data_group = models.CharField(max_length=255, blank=True, null=True)
    field_group = models.CharField(max_length=255, blank=True, null=True)
    field_snippet = models.CharField(max_length=255, blank=True, null=True)
    fl = models.CharField(max_length=255, blank=True, null=True)
    format_wt = models.CharField(max_length=255, blank=True, null=True)
    frag_snippet = models.IntegerField(blank=True, null=True)
    ip_dns = models.CharField(max_length=255)
    limit_group = models.IntegerField(blank=True, null=True)
    limit_results = models.IntegerField(blank=True, null=True)
    mm_1 = models.CharField(max_length=255, blank=True, null=True)
    mm_2 = models.CharField(max_length=255, blank=True, null=True)
    model_ltr = models.CharField(max_length=255, blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    port = models.CharField(max_length=255, blank=True, null=True)
    relevance = models.CharField(max_length=255, blank=True, null=True)
    size_snippet = models.IntegerField(blank=True, null=True)
    search_engine_config = models.OneToOneField(SearchEngineConfigs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_indexer_configs'


class SearchEngineLinkSectionItemConfigs(models.Model):
    link_section_id = models.BigAutoField(primary_key=True)
    field_link = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_link_section_item_configs'


class SearchEngineNavigateConfigs(models.Model):
    navigate_id = models.BigAutoField(primary_key=True)
    search_engine_config = models.OneToOneField(SearchEngineConfigs, models.DO_NOTHING, blank=True, null=True)
    style_config = models.OneToOneField('StyleConfigs', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_navigate_configs'


class SearchEngineOneboxConfigs(models.Model):
    onebox_config_id = models.BigAutoField(primary_key=True)
    order_ob = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_onebox_configs'


class SearchEngineResultsSectionConfigs(models.Model):
    results_section_config_id = models.BigAutoField(primary_key=True)
    content_field = models.CharField(max_length=255, blank=True, null=True)
    enable_thumbnail = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_custom_content = models.TextField(blank=True, null=True)  # This field type is a guess.
    thumbnail_field_url = models.CharField(max_length=255, blank=True, null=True)
    title_field = models.CharField(max_length=255, blank=True, null=True)
    url_field = models.CharField(max_length=255, blank=True, null=True)
    search_engine_config = models.OneToOneField(SearchEngineConfigs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_results_section_configs'


class SearchEngineSearchboxConfigs(models.Model):
    searchbox_id = models.BigAutoField(primary_key=True)
    has_spellchecker = models.TextField(blank=True, null=True)  # This field type is a guess.
    has_suggestions = models.TextField(blank=True, null=True)  # This field type is a guess.
    search_bar_icon = models.TextField(blank=True, null=True)
    search_bar_placeholder = models.CharField(max_length=255, blank=True, null=True)
    search_bar_type = models.CharField(max_length=255, blank=True, null=True)
    search_engine_config = models.OneToOneField(SearchEngineConfigs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_searchbox_configs'


class SearchEngineSpellcheckerConfigs(models.Model):
    spellchecker_id = models.BigAutoField(primary_key=True)
    name_spellchecker = models.CharField(max_length=255, blank=True, null=True)
    path_service_spellchecker = models.CharField(max_length=255, blank=True, null=True)
    type_spellchecker = models.CharField(max_length=255, blank=True, null=True)
    searchbox = models.OneToOneField(SearchEngineSearchboxConfigs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_spellchecker_configs'


class SearchEngineSuggestionConfigs(models.Model):
    suggestion_id = models.BigAutoField(primary_key=True)
    name_suggestion = models.CharField(max_length=255, blank=True, null=True)
    path_service_suggestion = models.CharField(max_length=255, blank=True, null=True)
    searchbox = models.OneToOneField(SearchEngineSearchboxConfigs, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'search_engine_suggestion_configs'


class SearchEngineToolBoxConfigs(models.Model):
    toolbox_configs_id = models.BigAutoField(primary_key=True)
    enable_date_relevance = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'search_engine_tool_box_configs'


class StyleConfigs(models.Model):
    style_config_id = models.BigAutoField(primary_key=True)
    background_color = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    font_family = models.CharField(max_length=255, blank=True, null=True)
    font_size = models.CharField(max_length=255, blank=True, null=True)
    font_style = models.CharField(max_length=255, blank=True, null=True)
    font_weight = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'style_configs'


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    username = models.CharField(unique=True, max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class UsersJoinOrganizations(models.Model):
    organization = models.ForeignKey(Organizations, models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(Users, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'users_join_organizations'
        unique_together = (('user', 'organization'),)


class UsersJoinRoles(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING)
    role = models.ForeignKey(Roles, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_join_roles'
        unique_together = (('user', 'role'),)
