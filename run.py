from app import create_app

run = create_app()

if __name__ == "__main__":
    run.run(debug=True)
