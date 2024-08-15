from flask import (
    Blueprint, flash, g, redirect, render_template, request, session
)

index_bp = Blueprint('index', __name__, url_prefix='/index')

from . import controllers