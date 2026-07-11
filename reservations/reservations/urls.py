{% extends 'catalogue/base.html' %}
{% block title %}Réserver{% endblock %}
{% block content %}
<h1>Réserver une place</h1>
<p><strong>{{ representation.show.title }}</strong> — {{ representation.schedule }}</p>

<form method="post" action="{% url 'reservation_store' representation.id %}" style="max-width: 400px;">
    {% csrf_token %}
    <div class="mb-3">
        <label class="form-label">Tarif</label>
        <select name="price_id" class="form-select" required>
            {% for price in prices %}
            <option value="{{ price.id }}">{{ price.type }} — {{ price.price }}€</option>
            {% endfor %}
        </select>
    </div>
    <div class="mb-3">
        <label class="form-label">Nombre de places</label>
        <input type="number" name="quantity" class="form-control" value="1" min="1" max="10" required>
    </div>
    <button type="submit" class="btn btn-primary">Confirmer la réservation</button>
</form>
{% endblock %}