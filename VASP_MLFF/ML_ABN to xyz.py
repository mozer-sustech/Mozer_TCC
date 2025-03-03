import argparse
import numpy as np
from ase import Atoms

def write_xyz(fid, images):
	for atoms in images:
		natoms = len(atoms)
		header = 'Lattice="%.16E %.16E %.16E %.16E %.16E %.16E %.16E %.16E %.16E" ' % tuple(atoms.cell.flatten())
		header += 'Properties=species:S:1:pos:R:3:forces:R:3 '
		header += 'name=%s ' % atoms.info['name']
		header += 'ctifor=%.16E ' % atoms.info['ctifor']
		header += 'energy=%.16E ' % atoms.info['energy']
		header += 'stress="%.16E %.16E %.16E %.16E %.16E %.16E %.16E %.16E %.16E"' % tuple(atoms.info['stress'].T.flatten())
		fid.write('%d\n%s\n' % (natoms, header))
		for s, (x,y,z), (fx,fy,fz) in zip(atoms.symbols, atoms.positions, atoms.arrays['forces']):
			fid.write('%2s %.16E %.16E %.16E %.16E %.16E %.16E\n' % (s, x,y,z, fx,fy,fz))

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

	parser.add_argument('input', type=str,
		help='input ML_AB file')

	parser.add_argument('output', type=str,
		help='output xyz file')

	args = parser.parse_args()

	images = read_ml_ab(args.input)

	write_xyz(open(args.output,'w'), images)