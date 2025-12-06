docker-compose exec postgres psql -U stride_user -d stride_db

docker-compose exec postgres psql -U stride_user -d stride_db -c "\dt"

docker-compose exec postgres psql -U stride_user -d stride_db -c "SELECT COUNT(*) as total_sneakers FROM sneaker;"

docker-compose exec postgres psql -U stride_user -d stride_db -c "SELECT sneaker_id, name, brand_id FROM sneaker LIMIT 5;"

# Database dump command
docker-compose exec -T postgres pg_dump -U stride_user stride_db | gzip > stride_db_dump.gz
