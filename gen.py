import os

class RegionCreator:
    def __init__(self):
        # initialise to a base value, used by all regions
        self.regionText = 'regions:'
        
        # initialise region specific details
        self.owner = ''
        self.startX = 0
        self.startZ = 0
        self.endX = 0
        self.endZ = 0
        self.members = ''
        self.flags = ''
        self.owners = ''
        self.type = 'cuboid'
        self.priority = 0

        self.minY = -64
        self.maxY = 319

        self.individualRegionSizeX = 0
        self.individualRegionSizeY = 0

        # a 'tab' as it were, YML doesn't like tabs though, so 4 spaces instead
        self.charSpace = '    '

        # request user inputs
        self.get_inputs()

    def get_inputs(self):
        print("Use this tool to generate regions for WorldGuard, provide the following information and the program will generate your file")
        print("Y value for each region is from -64 to 319")
        self.owner = input("What's the region naming scheme? (Whatever you put here will be followed by a number, e.g. 'Territory' will work out to be 'Territory1', 'Territory2' etc.): ")

        # try to parse details, if they can't be parsed the end the program
        try:
            self.startX = int(input("What's the starting X value for your overall region? : "))
            self.startZ = int(input("What's the starting Z value for your overall region? : "))
            self.endX = int(input("What's the ending X value for your overall region? : "))
            self.endZ = int(input("What's the ending Z value for your overall region? : "))
        except:
            print("Couldn't recognise integer input for value")
            exit()

        self.members = input("List the members of these regions (Leave blank for empty set): ")
        self.flags = input("Enter the flags you want in these regions (Leave blank for default): ")
        self.owners = input("Enter the owners of these regions (Leave blank for empty set): ")
        basePriority = input("Enter the priority (Leave blank for 0): ")
        # try to parse the priority, if it's empty or can't be parsed, default to 0
        try:
            self.priority = int(basePriority)
        except:
            self.priority = 0

        # request region size, try to parse to int, else end the program
        try:
            self.individualRegionSizeX = int(input("Enter the X size of each region: "))
            self.individualRegionSizeZ = int(input("Enter the Z size of each region: "))
        except:
            print("Couldn't recognise integer input for value")
            exit()

        # generate the regions
        self.generate_regions()
        
    def generate_region(self, regionNum, nextX, nextZ):
        # save some information about this particular region
        regionStartX = nextX
        regionStartZ = nextZ
        regionEndX = nextX + self.individualRegionSizeX
        regionEndZ = nextZ + self.individualRegionSizeZ

        # replace <region> with the name of this region, if applicable
        newFlags = self.flags.replace('<region>', self.owner + str(regionNum))

        # add this region to the regionText
        self.regionText += "\n" + self.charSpace + self.owner + str(regionNum) + ":"
        self.regionText += "\n" + self.charSpace + self.charSpace + "min: {x: " + str(regionStartX) + ", y: " + str(self.minY) + ", z: " + str(regionStartZ) + "}"
        self.regionText += "\n" + self.charSpace + self.charSpace + "max: {x: " + str(regionEndX) + ", y: " + str(self.maxY) + ", z: " + str(regionEndZ) + "}"
        self.regionText += "\n" + self.charSpace + self.charSpace + "members: {" + self.members + "}"
        self.regionText += "\n" + self.charSpace + self.charSpace + "flags: {" + newFlags + "}"
        self.regionText += "\n" + self.charSpace + self.charSpace + "owners: {" + self.owners + "}"
        self.regionText += "\n" + self.charSpace + self.charSpace + "type: " + self.type
        self.regionText += "\n" + self.charSpace + self.charSpace + "priority: " + str(self.priority)
        pass
    
    def generate_regions(self):
        # keep track of the number of regions, used for naming
        regionNum = 0
        # loop each x and z with a step of the individual region size plus some padding
        for x in range(self.startX, self.endX, self.individualRegionSizeX + 1):
            for z in range(self.startZ, self.endZ, self.individualRegionSizeZ + 1):
                # increase the region number
                regionNum += 1
                # generate this individual region
                self.generate_region(regionNum, x, z)

        # write the output to regions.yml
        with open(os.path.dirname(os.path.abspath(__file__)) + '/regions.yml', 'w') as f:
            f.write(self.regionText)
        # end the program
        exit()

# call the RegionCreator
RegionCreator()