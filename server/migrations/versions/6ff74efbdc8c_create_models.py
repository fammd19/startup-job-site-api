"""Create models

Revision ID: 6ff74efbdc8c
Revises: 
Create Date: 2024-07-30 19:38:28.023525

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ff74efbdc8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('_hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('abn', sa.Integer(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=False),
    sa.Column('industry', sa.String(), nullable=False),
    sa.Column('about', sa.String(), nullable=False),
    sa.Column('website_link', sa.String(), nullable=False),
    sa.Column('facebook_link', sa.String(), nullable=True),
    sa.Column('instagram_link', sa.String(), nullable=True),
    sa.Column('linkedin_link', sa.String(), nullable=True),
    sa.Column('admin_email', sa.String(), nullable=False),
    sa.Column('_hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abn'),
    sa.UniqueConstraint('admin_email'),
    sa.UniqueConstraint('name')
    )
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('salary', sa.Integer(), nullable=False),
    sa.Column('salary_comments', sa.String(), nullable=True),
    sa.Column('department', sa.String(), nullable=False),
    sa.Column('role_description', sa.String(), nullable=False),
    sa.Column('application_link', sa.String(), nullable=False),
    sa.Column('location', sa.String(), nullable=False),
    sa.Column('experience', sa.String(), nullable=True),
    sa.Column('closing_date', sa.DateTime(), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saved_jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=True),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], ),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('saved_jobs')
    op.drop_table('jobs')
    op.drop_table('companies')
    op.drop_table('candidates')
    # ### end Alembic commands ###
