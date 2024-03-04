from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Optional

class FilterForm(FlaskForm):
    f_rooms = IntegerField('Количество комнат', validators=[Optional()])
    f_district = StringField('Район', validators=[Optional()])
    f_metro = StringField('Станция метро', validators=[Optional()])
    f_author_type = SelectField('Тип продавца', validate_choice=False, choices=['Не выбрано', 'Агент', 'Официальный представитель', 'Риэлтор', 'Собственник'])
    f_area_lower = StringField('Нижняя граница площади', validators=[Optional()])
    f_area_upper = StringField('Верхняя граница площади', validators=[Optional()])
    f_price_lower = IntegerField('Нижняя граница цены', validators=[Optional()])
    f_price_upper = IntegerField('Верхняя граница цены', validators=[Optional()])
    f_submit = SubmitField('Submit')

class PublishForm(FlaskForm):
    p_author = StringField('Автор', validators=[DataRequired()])
    p_author_type = SelectField('Тип автора', validators=[DataRequired()],
    choices=[('real_estate_agent', 'Агент'), ('official_representative', 'Официальный представитель'),
    ('realtor', 'Риэлтор'), ('homeowner', 'Собственник')])
    p_link = StringField('Ссылка', validators=[DataRequired()])
    p_city = StringField('Город', validators=[DataRequired()])
    p_deal_type = StringField('Тип объявления', validators=[DataRequired()])
    p_accommodation_type = StringField('Тип жилья', validators=[DataRequired()])
    p_floor = IntegerField('Этаж', validators=[DataRequired()])
    p_floors_count = IntegerField('Всего этажей', validators=[DataRequired()])
    p_rooms_count = IntegerField('Число комнат', validators=[DataRequired()])
    p_total_meters = IntegerField('Площадь, кв. м', validators=[DataRequired()])
    p_price_per_month = IntegerField('Цена за месяц', validators=[DataRequired()])
    p_commissions = StringField('Комиссия', validators=[DataRequired()])
    p_district = StringField('Район', validators=[DataRequired()])
    p_street = StringField('Улица', validators=[DataRequired()])
    p_house_number = StringField('Дом', validators=[DataRequired()])
    p_underground = StringField('Метро', validators=[DataRequired()])
    p_submit = SubmitField('Submit')

class StatsForm1(FlaskForm):
    s1_sort = SelectField('Сортировать по', validators=[DataRequired()],
    choices=[('pricetotal', 'Цена за месяц'), ('area', 'Площадь, кв. м'), ('priceperm2', 'Цена за кв. м')])
    s1_direction = SelectField('Направление сортировки', validators=[DataRequired()],
    choices=[('up', 'По возрастанию'), ('down', 'По убыванию')])
    s1_sub = SubmitField('Submit')