<h1>Entrfy</h1>
<p>Django project for matching people based on their interests, using NoSQL, Graph technologies.</p>

<h3>How to run project</h3>
<ol>
  <li>Install Python 3.7 and Django and other dependencies in </li>
  <li>Set enviroment Variables (defined below) </li>
  <li>run neomodel_install_labels manage.py auth.models --db <NEO4J_DATABASE_URL> manually to setup neo4j schema</li>
  <li>Done!</li>
</ol>

<p>now you can run this on heroku (already setup) or on your local machine just by setting up the "DJANGO_SETTINGS_MODULE" to point to your prefered setting file [setting.local, settings.deployment]</p>

<h3>Required Enviroment variables</h3>
<ol>
  <li>"SECRET_KEY": Secure Secret key (the longer the better)</li>
  <li>"NEO4J_DATABASE_URL": neo4j connection string</li>
  <li>"MONGO_DATABASE_URL": mongo db connection string</li>
</ol>
