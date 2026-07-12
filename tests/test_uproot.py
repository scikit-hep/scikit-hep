def test_something():
    """Docstring explaining the test."""
    
    # 1. Pehle 'result' ko define karo (batao ye kya hai)
    result = len([1, 2, 3])  # Iska answer 3 aana chahiye
    
    # 2. Fir 'expected' ko define karo (jo aap chahte ho aana chahiye)
    expected = 3
    
    # 3. Ab computer check karega ki dono barabar hain ya nahi
    assert result == expected