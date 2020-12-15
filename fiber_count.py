def find_fiber_count(scale, fiber_radius=0.127, fiber_height=76.2,
                     collar=2.213479):
    """    Find Fiber Count, this function returns the estimated count of fibers.
    This is calculated by following these steps:
    Step 1. find weight of all fibers by subtracting the collar weight from
            Scale weight or 2.213479 grams.
    Step 2. Calculate weight of one fiber = pi() * radius^2 * height * Desity
    Step 3. Divide fibers weight from step one by weight of one fiber step 2.
    Step 4. Return the value from step 3. as an integer rounded up.

    The desnisty of AISI C1018 & C1065 is 0.00787(g/mm³) gram/mm³
    The collar is precalculated to be 2.213479 grams
    """
    # Step 1 - Find weight of all fibers
    fibers_weight = scale - collar

    # Step 2 - weight of one fiber
    fiber_weight = 3.141592 * fiber_radius**2 * fiber_height * 0.00787

    # Step 3 - Divide weight of all fibers by weight of one fiber to find count
    count = int(round(fibers_weight / fiber_weight, 0))

    return(count)


weight_from_scale = 31.785
rad = 0.127
lenth = 76.2

print(find_fiber_count(weight_from_scale, rad, lenth))
