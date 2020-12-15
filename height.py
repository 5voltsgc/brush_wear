def find_height(scale, fiber_radius=0.127, Num_fibers=974, collar=2.213479):
    """
    Find height returns the estimated height of the brush based on count of
    fibers, radius of one fiber, and scale weight following these steps:
    Step 1. find weight of all fibers by subtracting the collar weight from
            Scale weight or 2.213479 grams.
    Step 2. Divide weight by num_fibers to get weight of one fiber
    Step 3. Solve for height = one fiber weight/ pi() * r^2 *density
    Step 4. Return th height of the fibers


    The density of AISI C1018 & C1065 is 0.00787(g/mm³) gram/mm³
    The collar is precalculated to be 2.213479 grams
    """

    # Step 1. Find weight of all fibers
    fibers_weight = scale - collar

    # Step 2. Find weight of one fiber
    fiber_weight = fibers_weight / Num_fibers

    # Step 3. Solve for height of one fiber
    height = round(fiber_weight / (3.141592 * fiber_radius**2 * 0.00787), 8)
    return(height)


print(find_height(31.7863639892852, .127, 974))
