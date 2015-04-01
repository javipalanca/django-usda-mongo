from mongoengine import Document, IntField, StringField, BooleanField, FloatField, ReferenceField, ListField


FOOTNOTE_DESC = 'D'
FOOTNOTE_MEAS = 'M'
FOOTNOTE_NUTR = 'N'

FOOTNOTE_CHOICES = (
    (FOOTNOTE_DESC, 'Footnote adding information to the food  description'),
    (FOOTNOTE_MEAS, 'Footnote adding information to measure description'),
    (FOOTNOTE_NUTR, 'Footnote providing additional information on a nutrient value'),
)


class Food(Document):
    ndb_number = IntField(verbose_name='Nutrient Databank Number', primary_key=True, help_text='Nutrient Databank number that uniquely identifies a food item.')
    food_group = ReferenceField('FoodGroup', verbose_name='Food Group', help_text='Food group to which a food item belongs.')
    long_description = StringField(verbose_name='Long Description', max_length=200, help_text='Description of food item')
    short_description = StringField(verbose_name='Short Description', max_length=60, help_text='Description of food item')
    common_name = StringField(verbose_name='Common Name', max_length=100, help_text='Other names commonly used to describe a food, including local or regional names for various foods, for example, "soda" or "pop" for "carbonated beverages."')
    manufacturer_name = StringField(verbose_name='Manufacturer Name', max_length=65, help_text='Indicates the company that manufactured the product, when appropriate.')
    survey = BooleanField(verbose_name='Survey', default=False, help_text='Indicates if the food item is used in the USDA Food and Nutrient Database for Dietary Studies (FNDDS) and thus has a complete nutrient profile for the 65 FNDDS nutrients.')
    refuse_description = StringField(verbose_name='Refuse Description', max_length=135, help_text='Description of inedible parts of a food item (refuse), such as seeds or bone.')
    refuse_percentage = IntField(verbose_name='Refuse Percentage', null=True, help_text='Percentage of refuse.')
    scientific_name = StringField(verbose_name='Scientific Name', max_length=65, help_text='Scientific name of the food item. Given for the least processed form of the food (usually raw), if applicable.')
    nitrogen_factor = FloatField(verbose_name='Nitrogen Factor', null=True, help_text='Factor for converting nitrogen to protein.')
    protein_factor = FloatField(verbose_name='Protein Factor', null=True, help_text='Factor for calculating calories from protein.')
    fat_factor = FloatField(verbose_name='Fat Factor', null=True, help_text='Factor for calculating calories from fat.')
    cho_factor = FloatField(verbose_name='CHO Factor', null=True, help_text='Factor for calculating calories from carbohydrate.')

    class Meta:
        verbose_name = 'Food'
        verbose_name_plural = 'Foods'
        ordering = ['ndb_number']
        db_alias = 'usda'

    def __unicode__(self):
        return self.long_description

    def get_absolute_url(self):
        return 'usda-food_detail', (), {'ndb_number': self.ndb_number}


class FoodGroup(Document):
    code = IntField(verbose_name='Food Group Code', primary_key=True, help_text='Code identifying a food group. Codes may not be consecutive.')
    description = StringField(verbose_name='Description', max_length=60, help_text='Name of food group.')
    
    class Meta:
        verbose_name = 'Food Group'
        verbose_name_plural = 'Food Groups'
        ordering = ['code']
        db_alias = 'usda'

    def __unicode__(self):
        return self.description


class Nutrient(Document):
    number = IntField(verbose_name='Number', primary_key=True, help_text='Unique identifier code for a nutrient.')
    units = StringField(verbose_name='Units', max_length=7, help_text='Units of measure (mg, g, and so on).')
    tagname = StringField(verbose_name='Tagname', max_length=20, help_text='International Network of Food Data Systems (INFOODS) Tagnames. A unique abbreviation for a nutrient/food component developed by INFOODS to aid in the interchange of data.')
    description = StringField(verbose_name='Description', max_length=60, help_text='Name of nutrient/food component.')
    decimals = IntField(verbose_name='Decimals', help_text='Number of decimal places to which a nutrient value is rounded.')
    order = IntField(verbose_name='Order', help_text='Used to sort nutrient records in the same order as various reports produced from SR.')

    class Meta:
        verbose_name = 'Nutrient'
        verbose_name_plural = 'Nutrients'
        ordering = ['number']
        db_alias = 'usda'
    
    def __unicode__(self):
        return self.description


class NutrientData(Document):
    food = ReferenceField('Food', verbose_name='Food')
    nutrient = ReferenceField('Nutrient', verbose_name='Nutrient')
    nutrient_value = FloatField(verbose_name='Nutrient Value', help_text='Amount in 100 grams, edible portion.')
    data_points = IntField(verbose_name='Data Points', help_text='Number of data points (previously called Sample_Ct) is the number of analyses used to calculate the nutrient value. If the number of data points is 0, the value was calculated or imputed.')
    standard_error = FloatField(verbose_name='Standard Error', null=True, help_text='Standard error of the mean. Null if can not be calculated.')
    source = ListField(ReferenceField('Source', verbose_name='Source', help_text='Type of data'))
    data_derivation = ReferenceField('DataDerivation', verbose_name='Data Derivation', null=True, help_text='Data Derivation giving specific information on how the value is determined.')
    reference_nbd_number = IntField(verbose_name='Reference NBD Number', null=True, help_text='NDB number of the item used to impute a missing value. Populated only for items added or updated starting with SR14.')
    added_nutrient = BooleanField(verbose_name='Added Nutritient', default=False, help_text='Indicates a vitamin or mineral added for fortification or enrichment. This field is populated for ready-to-eat breakfast cereals and many brand-name hot cereals in food group 8.')
    number_of_studies = IntField(verbose_name='Number of Studies', null=True, help_text='Number of studies.')
    minimum = FloatField(verbose_name='Minimum', null=True, help_text='Minimum value.')
    maximum = FloatField(verbose_name='Maximum', null=True, help_text='Maximum value.')
    degrees_of_freedom = IntField(verbose_name='Degrees of Freedom', null=True, help_text='Degrees of freedom.')
    lower_error_bound = FloatField(verbose_name='Lower Error Bound.', null=True, help_text='Lower 95% error bound.')
    upper_error_bound = FloatField(verbose_name='Upper Error Bound.', null=True, help_text='Upper 95% error bound.')
    statistical_comments = StringField(verbose_name='Statistical Comments', max_length=10, help_text='Statistical comments.')
    confidence_code = StringField(verbose_name='Confidence Code', max_length=1, help_text='Confidence Code indicating data quality, based on evaluation of sample plan, sample handling, analytical method, analytical quality control, and number of samples analyzed. Not included in this release, but is planned for future releases.')

    class Meta:
        verbose_name = 'Nutrient Data'
        verbose_name_plural = 'Nutrient Data'
        ordering = ['food', 'nutrient']
        unique_together = ['food', 'nutrient']
        db_alias = 'usda'

    def __unicode__(self):
        return u'%s - %s' % (self.food, self.nutrient)


class Source(Document):
    code = IntField(verbose_name='Code', primary_key=True)
    description = StringField(verbose_name='Description', max_length=60, help_text='Description of source code that identifies the type of nutrient data.')

    class Meta:
        verbose_name = 'Source'
        verbose_name_plural = 'Sources'
        ordering = ['code']
        db_alias = 'usda'

    def __unicode__(self):
        return self.description


class DataDerivation(Document):
    code = StringField(verbose_name='Code', max_length=4, primary_key=True)
    description = StringField(verbose_name='Description', max_length=120, help_text='Description of derivation code giving specific information on how the value was determined.')

    class Meta:
        verbose_name = 'Data Derivation'
        verbose_name_plural = 'Data Derivations'
        ordering = ['code']
        db_alias = 'usda'

    def __unicode__(self):
        return self.description


class Weight(Document):
    food = ReferenceField('Food', verbose_name='Food')
    sequence = IntField(verbose_name='Sequence', help_text='Sequence number.')
    amount = FloatField(verbose_name='Amount', help_text='Unit modifier (for example, 1 in "1 cup").')
    description = StringField(verbose_name='Description', max_length=80, help_text='Description (for example, cup, diced, and 1-inch pieces).')
    gram_weight = FloatField(verbose_name='Gram Weight', help_text='Gram weight.')
    number_of_data_points = FloatField(verbose_name='Number of Data Points', null=True, help_text='Number of data points.')
    standard_deviation = FloatField(verbose_name='Standard Deviation', null=True, help_text='Standard Deviation')

    class Meta:
        verbose_name = 'Weight'
        verbose_name_plural = 'Weights'
        ordering = ['food', 'sequence']
        unique_together = ['food', 'sequence']
        db_alias = 'usda'

    def __unicode__(self):
        return u'%d %s %s %dg' % (self.amount, self.description, self.food, self.gram_weight)


class Footnote(Document):
    food = ReferenceField('Food', verbose_name='Food')
    number = IntField(verbose_name='Sequence', help_text='Sequence number. If a given footnote applies to more than one nutrient number, the same footnote number is used. As a result, this file cannot be indexed.')
    type = StringField(verbose_name='Type', max_length=1, choices=FOOTNOTE_CHOICES, help_text='Type of footnote.')
    nutrient = ReferenceField('Nutrient', verbose_name='nutrient', null=True)
    text = StringField(verbose_name='Text', max_length=200, help_text='Footnote text.')
    
    class Meta:
        verbose_name = 'Footnote'
        verbose_name_plural = 'Footnotes'
        ordering = ['food', 'number']
        unique_together = ['food', 'number', 'nutrient']
        db_alias = 'usda'
    
    def __unicode__(self):
        return self.text


class DataSource(Document):
    id = StringField(verbose_name='Id', max_length=6, primary_key=True, help_text='Unique number identifying the reference/source.')
    authors = StringField(verbose_name='Authors', max_length=255, help_text='List of authors for a journal article or name of sponsoring organization for other documents.')
    title = StringField(verbose_name='Title', max_length=255, help_text='Title of article or name of document, such as a report from a company or trade association.')
    year = IntField(verbose_name='Year', null=True, help_text='Year article or document was published.')
    journal = StringField(verbose_name='Journal', max_length=135, null=True, help_text='Name of the journal in which the article was published.')
    volume_or_city = StringField(verbose_name='Volume or City', max_length=16, help_text='Volume number for journal articles, books, or reports; city where sponsoring organization is located.')
    issue_or_state = StringField(verbose_name='Issue or State', max_length=5, help_text='Issue number for journal article; State where the sponsoring organization is located.')
    start_page = IntField(verbose_name='Start Page', null=True, help_text='Starting page number of article/document.')
    end_page = IntField(verbose_name='End Page', null=True, help_text='Ending page number of article/document.')

    class Meta:
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
        ordering = ['id']
        db_alias = 'usda'
    
    def __unicode__(self):
        return self.title