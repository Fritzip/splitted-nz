#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from django import forms
from app.models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = []

    zip = forms.FileField(required=False)