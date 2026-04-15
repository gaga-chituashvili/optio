def campaign_consumer(delta):
    for user_id in delta.added:
        print(f"Send promo to {user_id}")