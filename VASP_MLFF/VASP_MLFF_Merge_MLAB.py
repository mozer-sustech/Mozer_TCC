##For merging ML_AB files in VASP MLFF process
##Thanks to Prof. Li Pai. lipai@mail.sim.ac.cn
import argparse
import numpy as np

from ase import Atoms
from ase.io import read
from ase.data import atomic_masses, atomic_numbers
from collections.abc import Iterable

S1 = '**************************************************\n'
S2 = '--------------------------------------------------\n'
S3 = '==================================================\n'

def vasp_float(value, threshold=-1):
	string = ''
	if isinstance(value, Iterable):
		for v in value:
			if v != 0.0 and np.log10(np.abs(v)) < threshold:
				vs = np.format_float_scientific(v, precision=16, min_digits=16, exp_digits=3).replace('e','E')
				string += '%26s' % vs
			else:
				vs = np.format_float_positional(v, precision=16, min_digits=16, fractional=False)
				string += '%26s' % (vs + ' '*5)
	else:
		if value != 0.0 and np.log10(np.abs(value)) < threshold:
			vs = np.format_float_scientific(value, precision=16, min_digits=16, exp_digits=3).replace('e','E')
			string += '%26s' % vs
		else:
			vs = np.format_float_positional(value, precision=16, min_digits=16, fractional=False)
			string += '%26s' % (vs + ' '*5)

	return string

def write_label(fid, label):
	fid.write(S1)
	fid.write('     %s\n' % label)
	fid.write(S2)

def write_ml_ab(file, images):
	types = [a.get_chemical_symbols() for a in images]

	nconf = len(images)
	natoms = [len(t) for t in types]

	unique_types = []
	max_atoms_per_type = 0
	for t in types:
		n = np.max(np.unique(t, return_counts=True)[1])
		if n > max_atoms_per_type:
			max_atoms_per_type = n
		for e in t:
			if e not in unique_types:
				unique_types.append(e)

	ref_e = np.zeros(len(unique_types))
	basis = np.ones(len(unique_types))
	masses = atomic_masses[[atomic_numbers[t] for t in unique_types]]

	with open(file, 'w') as fid:
		fid.write(' 1.0 Version\n')
		write_label(fid, 'The number of configurations')
		fid.write('%11i\n' % nconf)

		write_label(fid, 'The maximum number of atom type')
		fid.write('%8i\n' % len(unique_types))

		write_label(fid, 'The atom types in the data file')
		for i in range(int(np.ceil(len(unique_types)/3))):
			fid.write('    ' + ' %-2s' * len(unique_types[3*i:3*i+3]) % tuple(unique_types[3*i:3*i+3]) + '\n')
		
		write_label(fid, 'The maximum number of atoms per system')
		fid.write('%15i\n' % np.max(natoms))

		write_label(fid, 'The maximum number of atoms per atom type')
		fid.write('%15i\n' % max_atoms_per_type)

		write_label(fid, 'Reference atomic energy (eV)')
		for i in range(int(np.ceil(len(ref_e)/3))):
			fid.write(vasp_float(ref_e[3*i:3*i+3]) + '\n')

		write_label(fid, 'Atomic mass')
		for i in range(int(np.ceil(len(masses)/3))):
			fid.write(vasp_float(masses[3*i:3*i+3]) + '\n')

		write_label(fid, 'The numbers of basis sets per atom type')
		for i in range(int(np.ceil(len(basis)/3))):
			fid.write('    ' + ' %5i' * len(basis[3*i:3*i+3]) % tuple(basis[3*i:3*i+3]) + '\n')

		for t in unique_types:
			write_label(fid, 'Basis set for %-2s' % t)
			fid.write('          1      1\n')

		for i,a in enumerate(images):
			symbols = np.array(a.get_chemical_symbols())
			unique_symbols = []
			for s in symbols:
				if s not in unique_symbols:
					unique_symbols.append(s)

			fid.write(S1)
			fid.write('     Configuration num. %6i\n' % (i+1))
			fid.write(S3)
			fid.write('     System name\n')
			fid.write(S2)
			fid.write('     %-40s\n' % a.info['name'])
			fid.write(S3)
			fid.write('     The number of atom types\n')
			fid.write(S2)
			fid.write('%8i\n' % len(np.unique(symbols)))
			fid.write(S3)
			fid.write('     The number of atoms\n')
			fid.write(S2)
			fid.write('%11i\n' % len(symbols))
			fid.write(S1)
			fid.write('     Atom types and atom numbers\n')
			fid.write(S2)
			for i in range(len(unique_symbols)):
				fid.write('     %-2s %6i\n' % (unique_symbols[i], np.sum(symbols==unique_symbols[i])))
			fid.write(S3)
			fid.write('     CTIFOR\n')
			fid.write(S2)
			fid.write(vasp_float(a.info['ctifor']) + '\n')
			fid.write(S3)
			fid.write('     Primitive lattice vectors (ang.)\n')
			fid.write(S2)
			for row in a.cell:
				fid.write(vasp_float(row) + '\n')
			fid.write(S3)
			fid.write('     Atomic positions (ang.)\n')
			fid.write(S2)
			for row in a.positions:
				fid.write(vasp_float(row) + '\n')
			fid.write(S3)
			fid.write('     Total energy (eV)\n')
			fid.write(S2)
			fid.write(vasp_float(a.info['energy']) + '\n')
			fid.write(S3)
			fid.write('     Forces (eV ang.^-1)\n')
			fid.write(S2)
			for row in a.arrays['forces']:
				fid.write(vasp_float(row) + '\n')
			fid.write(S3)
			fid.write('     Stress (kbar)\n')
			fid.write(S2)
			fid.write('     XX YY ZZ\n')
			fid.write(S2)
			fid.write(vasp_float(a.info['stress'][[0,1,2],[0,1,2]]) + '\n')
			fid.write(S2)
			fid.write('     XY YZ ZX\n')
			fid.write(S2)
			fid.write(vasp_float(a.info['stress'][[0,1,2],[1,2,0]]) + '\n')

def read_ml_ab(file):
	fid = open(file, 'r')
	lines = fid.readlines()
	fid.close()

	i = 0
	images = []
	while i < len(lines):
		line = lines[i].strip()

		# **************************************************
		# marks the begining of a section so we look for that

		if line == '**************************************************':
			i += 1
			line = lines[i].strip()
			if 'Configuration num.' in line:
				i += 4
				name = lines[i].strip()
	
				i += 4
				ntypes = int(lines[i].strip())
	
				i += 4
				natoms = int(lines[i].strip())
	
				i += 3
				symbols = []
				for _ in range(ntypes):
					i += 1
					line = lines[i].strip()
					data = line.split()
					symbols += [data[0]] * int(data[1])
	
				i += 4
				ctifor = float(lines[i].strip())
	
				i += 4
				data = ''.join(lines[i:i+3])
				cell = np.reshape(np.fromstring(data, sep=' '), (3,3))
	
				i += 6
				data = ''.join(lines[i:i+natoms])
				positions = np.reshape(np.fromstring(data, sep=' '), (natoms,3))
	
				i += natoms + 3
				energy = float(lines[i].strip())
	
				i += 4
				data = ''.join(lines[i:i+natoms])
				forces = np.reshape(np.fromstring(data, sep=' '), (natoms,3))
	
				i += natoms + 5
				s1 = np.fromstring(lines[i].strip(), sep=' ')
	
				i += 4
				s2 = np.fromstring(lines[i].strip(), sep=' ')
				stress = np.zeros((3,3))
	
				# XX YY ZZ
				stress[0,0] = s1[0]
				stress[1,1] = s1[1]
				stress[2,2] = s1[2]
	
				# XY YZ ZX
				stress[0,1] = s2[0]
				stress[1,2] = s2[1]
				stress[2,0] = s2[2]
	
				atoms = Atoms(
					symbols = symbols,
					positions = positions,
					cell = cell, pbc = (True,True,True),
					info = {
						'name': name,
						'ctifor': ctifor,
						'energy': energy,
						'stress': stress,
					}
				)
				atoms.arrays['forces'] = forces

				images.append(atoms)

		i += 1

	return images

if __name__ == '__main__':
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

	parser.add_argument('input', type=str, nargs='+',
		help='input ML_AB files')

	parser.add_argument('output', type=str,
		help='output ML_AB file')

	parser.add_argument('-s', '--skip', type=int, nargs='+',
		help='skip -s initial images, must be given for each input ML_AB file')

	args = parser.parse_args()
	images = []

	if args.skip != None and len(args.input) != len(args.skip):
		print('ERROR: -s must be given for each input ML_AB file')
		exit()

	if args.skip != None:
		for i,j in zip(args.input,args.skip):
			print('Reading %s, skipping %i' % (i,j))
			images += read_ml_ab(i)[j::]
	else:
		for i in args.input:
			print('Reading %s' % i)
			images += read_ml_ab(i)

	write_ml_ab(args.output, images)