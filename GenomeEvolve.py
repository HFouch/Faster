

from Class_extremities_and_adjacencies import Extremities_and_adjacencies

from Class_Evolve import Node_evolve
get_adjacencies = Extremities_and_adjacencies()
'''
genomeA = [[1,2,4,3]]
genomeB = [[1, 2,3,4, 5,6,7],[8,9, 10, 11, 12], [13, 14, 15]]


adjacencies_genomeA = get_adjacencies.adjacencies_ordered_and_sorted(genomeA)
adjacencies_genomeB = get_adjacencies.adjacencies_ordered_and_sorted(genomeB)

print('Adjacencies of the genomes: ')
print('Genome A: ', adjacencies_genomeA)
print('Genome B: ', adjacencies_genomeB)
print('____________________________________')
print()
print()





genome = Node_evolve(state=adjacencies_genomeB)
print(get_adjacencies.adjacencies_to_genome(genome.state))
print()
genome.evolve(num_inv=1, num_b_trl=1, num_fis=1, num_fus=1, num_trp1=1, num_trp2=0, num_u_trl=1)
print()
print(get_adjacencies.adjacencies_to_genome(genome.state))

'''
def evolve_genome(genomeB):
    adjacencies_genomeB = get_adjacencies.adjacencies_ordered_and_sorted(genomeB.copy())
    genome = Node_evolve(state=adjacencies_genomeB)

    genome.evolve(num_inv=4, num_b_trl=2, num_fis=1, num_fus=1, num_trp1=3, num_trp2=0, num_u_trl=2)


    return genome.state




