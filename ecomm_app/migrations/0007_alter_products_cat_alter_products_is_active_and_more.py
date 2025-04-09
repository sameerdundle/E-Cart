# Generated by Django 4.0 on 2025-04-03 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ecomm_app', '0006_products_pimage_alter_products_cat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='cat',
            field=models.IntegerField(choices=[(1, 'mobile'), (2, 'Shoes'), (3, 'Clothes')], verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='products',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Available'),
        ),
        migrations.AlterField(
            model_name='products',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Product Name'),
        ),
        migrations.AlterField(
            model_name='products',
            name='pdetails',
            field=models.CharField(max_length=20, verbose_name='Product_details'),
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecomm_app.products')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
        ),
    ]
