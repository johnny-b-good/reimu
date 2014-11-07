from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import sqlite3

app = Flask(__name__)
app.config.from_object('config')

def connect_db(): pass
def before_request(): pass
def teardown_request(exception): pass


def blog_page(): pass
def static_page(): pass
def admin_page(): pass
def sitemap_page(): pass

def login(): pass

def create_post(): pass
def read_post(): pass
def update_post(): pass
def delete_post(): pass

def create_comment(): pass
def delete_comment(): pass


if __name__ == '__main__':
    app.run()